# -*- coding: utf-8 -*-
"""
CineLocal Desktop - Inicializador Oficial em Modo Aplicativo
============================================================
Inicia o servidor CineLocal em segundo plano dentro do próprio processo
e abre uma janela de aplicativo nativa dedicada (Edge/Chrome/Brave em modo --app),
eliminando a barra de navegação e evitando qualquer abertura de múltiplas abas.
"""

import os
import sys
import time
import threading
import subprocess
import webbrowser
import urllib.request
import urllib.error
import multiprocessing

# Previne fork-bombs e múltiplas instâncias em executáveis PyInstaller no Windows
multiprocessing.freeze_support()

# Configuração de encoding UTF-8 no terminal
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Determina os diretórios base respeitando execução normal ou empacotada PyInstaller
if getattr(sys, "frozen", False):
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.executable))
    APP_DIR = os.path.join(ROOT_DIR, "app")
    if not os.path.exists(APP_DIR) and hasattr(sys, "_MEIPASS"):
        APP_DIR = os.path.join(sys._MEIPASS, "app")
else:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = os.path.join(ROOT_DIR, "app")

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

PORT = 8000
SERVER_URL = f"http://localhost:{PORT}/app/index.html"
HEALTH_URL = f"http://localhost:{PORT}/api/tools/status"

SERVER_THREAD = None

def is_server_running():
    """Verifica se o servidor CineLocal já está ativo e respondendo na porta 8000."""
    try:
        req = urllib.request.Request(f"http://localhost:{PORT}/api/status")
        with urllib.request.urlopen(req, timeout=0.8) as res:
            if res.status == 200:
                return True
    except Exception:
        pass
    return False

def start_server():
    """Inicia o servidor CineLocal dentro do próprio processo em thread separada (sem processos extras)."""
    global SERVER_THREAD
    if is_server_running():
        print("🍿 CineLocal já está ativo na porta 8000.")
        return True

    print("🚀 Iniciando motor CineLocal...")
    try:
        from servidor import run as start_server_main
        SERVER_THREAD = threading.Thread(
            target=start_server_main,
            kwargs={"open_browser": False},
            daemon=True
        )
        SERVER_THREAD.start()

        # Aguarda inicialização (até 5 segundos)
        for _ in range(25):
            time.sleep(0.2)
            if is_server_running():
                print("✅ Servidor CineLocal pronto!")
                return True

        return True
    except Exception as e:
        print(f"❌ Falha ao iniciar servidor interno: {e}")
        return False

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
    """Abre o CineLocal em uma única janela de aplicativo."""
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
            # Executa a janela do navegador e aguarda seu encerramento
            proc = subprocess.Popen(cmd)
            proc.wait()
            return
        except Exception as e:
            print(f"Aviso ao abrir modo app: {e}")

    # Fallback: se não tiver Chrome/Edge em modo app, abre exatamente UMA aba no navegador
    print("🌐 Abrindo no navegador padrão...")
    webbrowser.open(SERVER_URL)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    launch_desktop()
