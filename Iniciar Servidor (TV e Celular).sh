#!/usr/bin/env bash
# ==============================================================================
# CineLocal - Iniciar Servidor para TV e Celular (Linux e macOS)
# ==============================================================================
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

cd "$DIR/app"
"$PYTHON_CMD" servidor.py "$@"
