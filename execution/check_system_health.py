#!/usr/bin/env python3
import os
import sys
import json

def main():
    """
    Valida la integridad del sistema verificando que la estructura de carpetas
    y archivos esenciales existan.
    """
    # Determinar la raíz del proyecto (asumiendo que este script está en execution/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Definir la estructura esperada según la arquitectura
    required_structure = {
        "directories": [
            "directives",
            "execution",
            ".tmp",
            ".gemini"
        ],
        "files": [
            ".env",
            "README.md",
            "execution/alert_user.py"
        ]
    }

    health_report = {
        "status": "ok",
        "checks": {},
        "errors": []
    }

    # 1. Validar Directorios
    for directory in required_structure["directories"]:
        path = os.path.join(project_root, directory)
        if os.path.isdir(path):
            health_report["checks"][directory] = "ok"
        else:
            health_report["checks"][directory] = "missing"
            health_report["errors"].append(f"Falta el directorio: {directory}")

    # 2. Validar Archivos
    for filename in required_structure["files"]:
        path = os.path.join(project_root, filename)
        if os.path.isfile(path):
            health_report["checks"][filename] = "ok"
        else:
            health_report["checks"][filename] = "missing"
            health_report["errors"].append(f"Falta el archivo: {filename}")

    # 3. Emitir resultado
    is_healthy = len(health_report["errors"]) == 0
    health_report["status"] = "ok" if is_healthy else "error"
    
    print(json.dumps(health_report, indent=2))
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()