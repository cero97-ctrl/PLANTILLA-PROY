# Changelog

Todas las mejoras notables de este proyecto serán documentadas en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Añadido
- Script `execution/check_system_health.py` para validación de entorno (Python, .env, dependencias).
- Mejora en `generate_readme.py`: ahora lee los archivos YAML para incluir la descripción (`goal`) de cada directiva en el prompt del LLM.
- Integración con Telegram: `execution/telegram_tool.py` y directiva `telegram_remote_control.yaml` para control remoto y notificaciones.
- Nueva acción `get-id` en `telegram_tool.py` para facilitar la configuración inicial del Chat ID.
- Nuevos comandos en `listen_telegram.py`: `/recordar` (memoria) y `/ayuda`.
- Activación de RAG en `chat_with_llm.py`: ahora consulta automáticamente ChromaDB para inyectar contexto de memoria en las respuestas.
- Depuración de RAG: `chat_with_llm.py` ahora muestra errores de memoria en stderr.
- Gestión de memoria: añadido `delete_memory.py` y comando `/olvidar` en Telegram.
- Mejora en `listen_telegram.py`: ahora muestra los logs de error (stderr) de los subprocesos para facilitar la depuración.
- Robustez en `telegram_tool.py`: añadido fallback automático a texto plano si falla el envío por formato Markdown.
- **Bug Fix Crítico**: Corregido error en `chat_with_llm.py` donde el contexto de memoria recuperado (RAG) no se enviaba al LLM.
- Nuevo comando `/memory` en `run_agent.py` para consultar la memoria desde el CLI principal.
- Mejora de RAG en `/investigar`: ahora el agente cruza los resultados de búsqueda con su memoria interna antes de resumir.
- Mejora en logs de `chat_with_llm.py`: ahora muestra una previsualización del recuerdo recuperado para facilitar la depuración.

## [1.0.0] - 2026-02-16
### Añadido
- Arquitectura de 3 capas (Directivas, Orquestación, Ejecución).
- Integración con LLMs (OpenAI, Anthropic, Google Gemini).
- Sistema de memoria vectorial local con ChromaDB.
- Herramientas de desarrollo: `init_project`, `pre_commit_check`, `deploy_to_github`.
- Soporte para interfaz de voz y traducción de documentos.
- Documentación completa y guías de contribución.
