#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests
import warnings

# Suppress warnings to ensure clean JSON output
warnings.filterwarnings("ignore")

# Intentar importar SDK de Google
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Intentar importar ChromaDB para memoria a largo plazo
try:
    import chromadb
except ImportError:
    chromadb = None

# Intentar cargar variables de entorno si python-dotenv está instalado
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(usecwd=True))
except ImportError:
    pass

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".tmp", "chat_history.json")


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_memory_context(query):
    """Busca contexto relevante en la memoria vectorial (ChromaDB)."""
    if not chromadb:
        print("⚠️  [RAG] ChromaDB no instalado o no importado.", file=sys.stderr)
        return None
        
    try:
        # Ruta a la base de datos (mismo path que save_memory.py)
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".tmp", "chroma_db")
        
        if not os.path.exists(db_path):
            print(f"⚠️  [RAG] No se encontró base de datos en: {db_path}", file=sys.stderr)
            return None

        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection(name='agent_memory')
        
        results = collection.query(
            query_texts=[query],
            n_results=3 # Recuperar los 3 recuerdos más relevantes
        )
        
        documents = results.get('documents', [[]])[0]
        if documents:
            preview = documents[0][:60] + "..." if len(documents[0]) > 60 else documents[0]
            print(f"🧠 [RAG] Contexto inyectado ({len(documents)} items): '{preview}'", file=sys.stderr)
            return "\n".join([f"- {doc}" for doc in documents])
        else:
            print("🧠 [RAG] No se encontraron recuerdos relevantes para esta consulta.", file=sys.stderr)
    except Exception as e:
        print(f"❌ [RAG] Error al consultar memoria: {e}", file=sys.stderr)
    return None

def chat_openai(messages, model="gpt-4o-mini"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "Falta OPENAI_API_KEY en .env"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un asistente de IA útil actuando como la capa de Orquestación en una arquitectura de 3 capas."}
        ] + messages,
        "temperature": 0.7
    }

    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return {"content": result['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}


def chat_anthropic(messages, model="claude-3-5-sonnet-20240620"):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "Falta ANTHROPIC_API_KEY en .env"}

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
        "system": "Eres un asistente de IA útil actuando como la capa de Orquestación en una arquitectura de 3 capas."
    }

    try:
        resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return {"content": result['content'][0]['text']}
    except Exception as e:
        return {"error": str(e)}


def chat_gemini(messages, model="gemini-flash-latest"):
    if not genai:
        return {"error": "Librería 'google-generativeai' no instalada. Ejecuta: pip install -r requirements.txt"}

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "Falta GOOGLE_API_KEY en .env"}

    try:
        genai.configure(api_key=api_key)

        # Preparar historial y system instruction
        system_instruction = "Eres Gemini, un modelo de IA de Google, actuando como la capa de Orquestación en una arquitectura de 3 capas. Identifícate siempre como Gemini/Google si te preguntan."
        history = []

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                history.append({"role": "model", "parts": [msg["content"]]})

        # Extraer el último mensaje del usuario para enviarlo (el SDK maneja el historial aparte)
        if not history or history[-1]["role"] != "user":
            return {"error": "El historial debe terminar con un mensaje del usuario."}

        last_message = history.pop()

        # Estrategia de Fallback: Intentar modelos alternativos si el principal falla
        models_to_try = [model]
        # Lista de modelos seguros para probar en orden si el principal falla
        fallbacks = ["gemini-1.5-flash", "gemini-pro", "gemini-flash-latest"]
        for fb in fallbacks:
            if fb != model:
                models_to_try.append(fb)

        last_error = None
        for target_model in models_to_try:
            try:
                model_instance = genai.GenerativeModel(model_name=target_model, system_instruction=system_instruction)
                chat = model_instance.start_chat(history=history)
                response = chat.send_message(last_message["parts"][0])
                return {"content": response.text}
            except Exception as e:
                print(f"⚠️  Advertencia: Falló {target_model} ({e}). Intentando siguiente...", file=sys.stderr)
                last_error = e
                continue

        return {"error": f"Todos los modelos fallaron. Último error: {str(last_error)}"}

    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Enviar un prompt a un LLM (OpenAI/Anthropic).")
    parser.add_argument("--prompt", required=True, help="El mensaje para el LLM.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "gemini"], help="Proveedor de IA.")
    args = parser.parse_args()

    # Gestión de historial
    if args.prompt.strip().lower() == "/clear":
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        print(json.dumps({"content": "Historial de conversación borrado."}))
        return

    history = load_history()
    # Mantener contexto corto (últimos 10 mensajes) para evitar errores de tokens
    if len(history) > 10:
        history = history[-10:]

    history.append({"role": "user", "content": args.prompt})

    # --- RAG: Inyección de Memoria ---
    # Creamos una copia de los mensajes para enviar al LLM con el contexto inyectado,
    # pero SIN ensuciar el historial guardado en disco.
    messages_for_llm = [dict(msg) for msg in history] # Deep copy simple
    
    memory_context = get_memory_context(args.prompt)
    if memory_context:
        # Inyectamos el contexto en el último mensaje del usuario
        last_msg = messages_for_llm[-1]
        last_msg['content'] = f"CONTEXTO DE MEMORIA (Recuerdos relevantes):\n{memory_context}\n\n---\nPREGUNTA DEL USUARIO:\n{args.prompt}"

    # Selección automática de proveedor si no se especifica
    provider = args.provider
    if not provider:
        if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_API_KEY").strip():
            provider = "gemini"
        elif os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY").strip():
            provider = "openai"
        elif os.getenv("ANTHROPIC_API_KEY") and os.getenv("ANTHROPIC_API_KEY").strip():
            provider = "anthropic"
        else:
            provider = "openai"  # Default

    if provider == "openai":
        result = chat_openai(messages_for_llm)
    elif provider == "anthropic":
        result = chat_anthropic(messages_for_llm)
    else:
        result = chat_gemini(messages_for_llm)

    if "content" in result:
        history.append({"role": "assistant", "content": result["content"]})
        save_history(history)

    # Salida en JSON para que el orquestador la consuma
    print(json.dumps(result))


if __name__ == "__main__":
    main()
