# -*- coding: utf-8 -*-
"""
CineLocal - Construtor de Pacote Desktop e Executável Windows (Issue #17 & #18)
==============================================================================
Compila o CineLocal em um executável autônomo (.exe) sem terminal visível
e prepara o instalador oficial via Inno Setup (CineLocal-Setup-v2.5.exe).
"""

import os
import sys
import shutil
import struct
import subprocess

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
SPEC_FILE = os.path.join(ROOT_DIR, "CineLocal.spec")
ICO_FILE = os.path.join(APP_DIR, "icon.ico")
PNG_FILE = os.path.join(APP_DIR, "icon-192.png")
ISS_FILE = os.path.join(ROOT_DIR, "installer", "CineLocal.iss")

def ensure_icon():
    """Garante que o arquivo icon.ico exista gerando a partir de icon-192.png se necessário."""
    if os.path.exists(ICO_FILE):
        return ICO_FILE

    if os.path.exists(PNG_FILE):
        print("🎨 Gerando icon.ico a partir de icon-192.png...")
        with open(PNG_FILE, 'rb') as f:
            png_data = f.read()

        header = struct.pack('<HHH', 0, 1, 1)
        entry = struct.pack('<BBBBHHII', 192, 192, 0, 0, 1, 32, len(png_data), 6 + 16)
        with open(ICO_FILE, 'wb') as f:
            f.write(header + entry + png_data)
        return ICO_FILE

    return None

def generate_spec_file():
    """Cria a especificação CineLocal.spec para o PyInstaller."""
    root_path_clean = ROOT_DIR.replace("\\", "/")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('app', 'app'),
    ('README.md', '.')
]

a = Analysis(
    ['run_desktop.py'],
    pathex=['{root_path_clean}', '{root_path_clean}/app'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'servidor',
        'tools_manager',
        'atualizar_catalogo',
        'metadata_db',
        'http.server',
        'socketserver',
        'urllib.request',
        'urllib.parse',
        'json',
        'threading',
        'multiprocessing',
        'shutil',
        'subprocess',
        'sqlite3'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CineLocal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CineLocal'
)
'''
    with open(SPEC_FILE, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("📝 Especificação CineLocal.spec gerada com sucesso!")

def find_inno_setup():
    """Procura o compilador do Inno Setup (iscc.exe)."""
    in_path = shutil.which("iscc") or shutil.which("iscc.exe")
    if in_path:
        return in_path

    prog_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    prog_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    candidates = [
        os.path.join(prog_files_x86, "Inno Setup 6", "ISCC.exe"),
        os.path.join(prog_files, "Inno Setup 6", "ISCC.exe"),
        os.path.join(prog_files_x86, "Inno Setup 5", "ISCC.exe"),
        os.path.join(prog_files, "Inno Setup 5", "ISCC.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def build():
    print("=" * 70)
    print("🎬 CINELOCAL - CONSTRUTOR DE EXECUTÁVEL E INSTALADOR WINDOWS")
    print("=" * 70)

    ensure_icon()
    generate_spec_file()

    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"📦 PyInstaller detectado: versão {PyInstaller.__version__}")
    except ImportError:
        print("💡 Instalando PyInstaller no ambiente...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    print("\n🔨 Compilando CineLocal.exe com PyInstaller...")
    workpath = os.path.join(os.environ.get("TEMP", os.environ.get("LOCALAPPDATA", "C:\\Temp")), "pyi_cinelocal_work")
    os.makedirs(workpath, exist_ok=True)
    subprocess.run([sys.executable, "-m", "PyInstaller", SPEC_FILE, "--workpath", workpath, "--clean", "-y"], check=True)

    exe_path = os.path.join(DIST_DIR, "CineLocal", "CineLocal.exe")
    if os.path.exists(exe_path):
        print(f"\n✅ Executável CineLocal.exe construído com sucesso!")
        print(f"   Local: {exe_path}")
        print(f"   Tamanho: {os.path.getsize(exe_path) / 1024:.1f} KB")

    # Verifica Inno Setup para gerar instalador .exe
    iscc = find_inno_setup()
    if iscc and os.path.exists(ISS_FILE):
        print(f"\n📦 Compilando instalador oficial com Inno Setup ({iscc})...")
        out_dir = os.path.join(DIST_DIR, "installer")
        os.makedirs(out_dir, exist_ok=True)
        subprocess.run([iscc, ISS_FILE], check=True)
        print("🎉 Instalador criado com sucesso em dist/installer/CineLocal-Setup-v2.5.0.exe!")
    else:
        print("\n💡 Dica sobre o Instalador:")
        print("   O executável portátil 'CineLocal.exe' já está 100% pronto em dist/CineLocal/CineLocal.exe!")
        print("   Para empacotar em assistente de instalação (CineLocal-Setup.exe):")
        print("   1. Baixe o Inno Setup gratuito: https://jrsoftware.org/isdl.php")
        print("   2. Abra 'installer/CineLocal.iss' e clique em Compile (F9).")

    print("\n" + "=" * 70)
    print("✨ Processo de compilação desktop finalizado com sucesso!")
    print("=" * 70)

if __name__ == "__main__":
    build()
