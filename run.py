# -*- coding: utf-8 -*-
"""
CineLocal - Inicializador Unificado na Raiz
Execute: python run.py
"""
import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")
SERVER_PY = os.path.join(APP_DIR, "servidor.py")

if __name__ == '__main__':
    if os.path.exists(SERVER_PY):
        os.chdir(APP_DIR)
        try:
            subprocess.run([sys.executable, SERVER_PY])
        except KeyboardInterrupt:
            print("\nCineLocal finalizado.")
    else:
        print(f"Erro: Arquivo do servidor não encontrado em {SERVER_PY}")
