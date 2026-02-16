#!/usr/bin/env python3
import argparse
import json
import sys

try:
    import chromadb
except ImportError:
    print("Error: Missing 'chromadb'.", file=sys.stderr)
    sys.exit(10)

def main():
    parser = argparse.ArgumentParser(description="Eliminar un recuerdo por ID.")
    parser.add_argument("--id", required=True, help="ID del recuerdo a eliminar.")
    parser.add_argument("--db-path", default=".tmp/chroma_db", help="Ruta a ChromaDB.")
    args = parser.parse_args()

    try:
        client = chromadb.PersistentClient(path=args.db_path)
        collection = client.get_or_create_collection(name="agent_memory")
        
        # ChromaDB lanza error si el ID no existe en algunas versiones, en otras no hace nada.
        collection.delete(ids=[args.id])
        
        print(json.dumps({
            "status": "success", 
            "message": f"Recuerdo {args.id} eliminado correctamente."
        }))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()