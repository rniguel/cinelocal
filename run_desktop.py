# -*- coding: utf-8 -*-
"""
CineLocal Desktop - Inicializador Oficial em Modo Aplicativo
============================================================
Inicia o servidor CineLocal em segundo plano e abre uma janela de aplicativo
nativa dedicada (Edge/Chrome/Brave em modo --app), eliminando a barra de navegação
e proporcionando uma experiência cinematográfica 100% autônoma.
"""

import os
import sys
import time
import subprocess
import webbrowser
import urllib.request
import urllib.error
import atexit

# Configuração de encoding UTF-8 no terminal
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")
SERVER_SCRIPT = os.path.join(APP_DIR, "servidor.py")
PORT = 8000
SERVER_URL = f"http://localhost:{PORT}/app/index.html"
HEALTH_URL = f"http://localhost:{PORT}/api/tools/status"

SERVER_PROC = None

def is_server_running():
    """Verifica se o servidor CineLocal já está ativo e respondendo."""
    try:
        req = urllib.request.Request(f"http://localhost:{PORT}/api/status")
        with urllib.request.urlopen(req, timeout=1.2) as res:
            if res.status == 200:
                return True
    except Exception:
        pass
    return False

def start_server():
    """Inicia o servidor CineLocal em segundo plano caso não esteja rodando."""
    global SERVER_PROC
    if is_server_running():
        print("🍿 CineLocal já está ativo na porta 8000.")
        return True

    print("🚀 Iniciando motor CineLocal...")
    python_bin = sys.executable

    creationflags = 0
    if sys.platform == "win32":
        # Esconde a janela de terminal do subprocesso no Windows
        creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0x08000000

    try:
        SERVER_PROC = subprocess.Popen(
            [python_bin, SERVER_SCRIPT],
            cwd=ROOT_DIR,
            creationflags=creationflags
        )

        # Aguarda inicialização (até 6 segundos)
        for _ in range(30):
            time.sleep(0.2)
            if is_server_running():
                print("✅ Servidor CineLocal pronto!")
                return True

        print("⚠️ Servidor demorou para responder, tentando abrir assim mesmo...")
        return True
    except Exception as e:
        print(f"❌ Falha ao iniciar servidor: {e}")
        return False

def cleanup_server():
    """Encerra o servidor ao fechar o aplicativo desktop."""
    global SERVER_PROC
    if SERVER_PROC and SERVER_PROC.poll() is None:
        try:
            SERVER_PROC.terminate()
            SERVER_PROC.wait(timeout=2)
        except Exception:
            pass

atexit.register(cleanup_server)

def find_app_browser():
    """Localiza navegadores capazes de rodar em modo aplicativo nativo (--app)."""
    candidates = []

    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        candidates = [
            # Microsoft Edge (Nativo em 100% dos PCs Windows 10/11)
            os.path.join(prog_files_x86, "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(prog_files, "Microsoft", "Edge", "Application", "msedge.exe"),
            # Google Chrome
            os.path.join(prog_files, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(prog_files_x86, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(local_app_data, "Google", "Chrome", "Application", "chrome.exe"),
            # Brave Browser
            os.path.join(prog_files, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
            os.path.join(local_app_data, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
    else:
        # Linux
        candidates = [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "microsoft-edge-stable",
            "brave-browser"
        ]

    for c in candidates:
        if sys.platform in ("win32", "darwin"):
            if os.path.exists(c):
                return c
        else:
            import shutil
            found = shutil.which(c)
            if found:
                return found

    return None

def launch_desktop():
    """Abre o CineLocal na melhor interface possível."""
    start_server()

    browser = find_app_browser()
    if browser:
        print(f"🎬 Abrindo janela CineLocal Desktop ({os.path.basename(browser)})...")
        app_arg = f"--app={SERVER_URL}"
        user_data_dir = os.path.join(APP_DIR, "data", "browser_profile")
        os.makedirs(user_data_dir, exist_ok=True)
        profile_arg = f"--user-data-dir={user_data_dir}"

        cmd = [browser, app_arg, profile_arg, "--start-maximized"]
        try:
            # Executa a janela do navegador em primeiro plano
            proc = subprocess.Popen(cmd)
            proc.wait()
            return
        except Exception as e:
            print(f"Aviso ao abrir modo app: {e}")

    # Fallback para navegador padrão
    print("🌐 Abrindo no navegador padrão...")
    webbrowser.open(SERVER_URL)
    # Mantém o processo vivo se o servidor for filho
    if SERVER_PROC:
        try:
            SERVER_PROC.wait()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    launch_desktop()
