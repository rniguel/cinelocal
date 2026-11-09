#!/usr/bin/env bash
# ==============================================================================
# CineLocal - Inicializador Desktop para Linux e macOS
# ==============================================================================

set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "======================================================="
echo "          Iniciando CineLocal Desktop"
echo "======================================================="
echo ""

if command -v python3 &>/dev/null; then
    python3 run_desktop.py
elif command -v python &>/dev/null; then
    python run_desktop.py
else
    echo "❌ Python não encontrado no sistema."
    exit 1
fi
