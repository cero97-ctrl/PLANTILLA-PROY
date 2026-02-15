# [Nombre del Proyecto]

## Descripción
<!-- Proporciona una descripción breve y clara de qué hace este proyecto y qué problema resuelve. -->
Este proyecto es una implementación basada en el **Gemini Agent Framework**, diseñado para...

## Requisitos Previos

- **Python 3.10+**
- **Conda** (Recomendado para gestión de entornos)
- **Clave de API** (Configurada en `.env`)

## Inicialización del Proyecto (Desde Plantilla)

Para comenzar un nuevo desarrollo basado en este framework:

1.  **Clonar la plantilla:**
    ```bash
    git clone <URL_DEL_REPOSITORIO> <NOMBRE_NUEVO_PROYECTO>
    cd <NOMBRE_NUEVO_PROYECTO>
    ```

2.  **Ejecutar configuración automática:**
    Este script crea el entorno Conda, instala dependencias e inicializa el proyecto.
    ```bash
    bash setup.sh
    ```

3.  **Configurar credenciales:**
    Edita el archivo `.env` generado y añade tus API Keys.

4.  **Activar entorno:**
    Para empezar a trabajar en futuras sesiones:
    ```bash
    conda activate agent_env
    ```

## Uso

<!-- Instrucciones sobre cómo ejecutar el proyecto o interactuar con el agente -->
Para iniciar el flujo principal:
```bash
# Ejemplo de comando
python execution/run_agent.py
```

## Arquitectura del Agente
Este proyecto utiliza una arquitectura de 3 capas (Directivas, Orquestación, Ejecución). Para detalles técnicos sobre cómo operar o extender el agente, consulta:

- [Instrucciones del Agente](.gemini/instructions.md)
- [Framework y Filosofía](.gemini/AGENT_FRAMEWORK.md)

## Herramientas de Desarrollo
Este framework incluye herramientas para facilitar tareas comunes:

- **`init_project.py`**: Script para limpiar y configurar un nuevo proyecto desde esta plantilla.
- **`create_new_directive.yaml`**: Directiva para generar automáticamente el esqueleto de nuevas directivas.
- **`update_template.yaml`**: Directiva para traer actualizaciones desde el repositorio plantilla original.
- **`deploy_to_github.yaml`**: Automatiza el flujo de git add/commit/push para reportar avances.

## Reportar Avances (Git)
Para guardar tu trabajo y subirlo a GitHub, puedes usar la herramienta de despliegue incluida:

1.  **Primera subida (si reiniciaste el historial):**
    ```bash
    python execution/deploy_to_github.py --message "Entrega inicial" --remote <URL_TU_REPO>
    ```

2.  **Avances diarios:**
    ```bash
    python execution/deploy_to_github.py --message "Implementando función X"
    ```

## Mantenimiento y Contribución
Si deseas proponer cambios o mejoras, consulta la [Guía de Contribución](CONTRIBUTING.md).

Para mantener este proyecto actualizado con la plantilla original, puedes utilizar la directiva `directives/update_template.yaml`. Esta herramienta permite al agente traer los últimos cambios del repositorio base y fusionarlos con tu trabajo actual.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.