# -*- coding: utf-8 -*-
"""
🎬 CINELOCAL - GERENCIADOR & INSTALADOR AUTOMÁTICO SAMSUNG SMART TV (TIZEN OS)
Empacota o aplicativo .wgt assinado com o perfil oficial Samsung e instala na TV via rede Wi-Fi.
"""

import os
import sys
import shutil
import zipfile
import subprocess
import socket
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIZEN_SRC = os.path.join(BASE_DIR, "tizen")
DIST_DIR = os.path.join(BASE_DIR, "dist")
OUTPUT_WGT = os.path.join(DIST_DIR, "CineLocal.wgt")

USER_HOME = os.path.expanduser("~")
TIZEN_PLATFORM_DIR = os.path.join(USER_HOME, ".tizen-extension-platform")
SDB_BIN = os.path.join(TIZEN_PLATFORM_DIR, "server", "sdktools", "data", "tools", "sdb.exe")
TZ_BIN = os.path.join(TIZEN_PLATFORM_DIR, "server", "sdktools", "data", "tools", "tizen-core", "tz.exe")
CERT_MGR_BIN = os.path.join(TIZEN_PLATFORM_DIR, "server", "sdktools", "data", "tools", "certificate-manager", "certificate-manager.exe")
DEV_MGR_BIN = os.path.join(TIZEN_PLATFORM_DIR, "server", "sdktools", "data", "tools", "device-manager", "device-manager.exe")
PROFILE_NAME = "Cinelocal"
PACKAGE_ID = "cinelocal1"
APP_ID = "cinelocal1.CineLocal"

def banner():
    print("=" * 68)
    print("📺 CINELOCAL - GERENCIADOR SAMSUNG SMART TV (TIZEN OS)")
    print("=" * 68)

def get_local_pc_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def check_sdk_status():
    has_sdb = os.path.exists(SDB_BIN)
    has_tz = os.path.exists(TZ_BIN)
    has_cert = os.path.exists(CERT_MGR_BIN)
    has_dev = os.path.exists(DEV_MGR_BIN)

    print("🔍 DIAGNÓSTICO DO AMBIENTE TIZEN:")
    print(f"   • SDB (Smart Development Bridge): {'✅ Detectado' if has_sdb else '❌ Não encontrado'}")
    print(f"   • Tizen CLI (tz.exe):             {'✅ Detectado' if has_tz else '❌ Não encontrado'}")
    print(f"   • Gerenciador de Certificados:    {'✅ Detectado' if has_cert else '❌ Não encontrado'}")
    print(f"   • Gerenciador de Dispositivos:    {'✅ Detectado' if has_dev else '❌ Não encontrado'}")
    print(f"   • IP deste computador na rede:    🌐 {get_local_pc_ip()}")
    print("-" * 68)
    return has_sdb

def clean_build_artifacts():
    rds = os.path.join(TIZEN_SRC, ".tizen-rds")
    debug = os.path.join(TIZEN_SRC, "Debug")
    for d in (rds, debug):
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)

def package_wgt(profile=PROFILE_NAME):
    os.makedirs(DIST_DIR, exist_ok=True)
    if not os.path.exists(TIZEN_SRC):
        print(f"❌ Diretório fonte '{TIZEN_SRC}' não encontrado!")
        return False

    clean_build_artifacts()

    if os.path.exists(TZ_BIN):
        print(f"🔐 Empacotando e assinando com o perfil Samsung '{profile}' via tz.exe...")
        cmd = [TZ_BIN, "pack", "-w", TIZEN_SRC, "-t", "wgt", "-s", profile, "-o", OUTPUT_WGT]
        res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
        debug_wgt = os.path.join(TIZEN_SRC, "Debug", "tizen.wgt")
        if os.path.exists(debug_wgt):
            shutil.copy2(debug_wgt, OUTPUT_WGT)
            size_kb = round(os.path.getsize(OUTPUT_WGT) / 1024, 1)
            print(f"✅ Pacote assinado com sucesso: {OUTPUT_WGT} ({size_kb} KB)")
            print("-" * 68)
            return True
        else:
            print(f"⚠️ Erro ao assinar pacote:\n{res.stdout}\n{res.stderr}")

    print("⚠️ tz.exe indisponível ou falhou, gerando pacote zip simples...")
    files_to_pack = []
    for root, _, files in os.walk(TIZEN_SRC):
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, TIZEN_SRC)
            files_to_pack.append((fp, rel))

    with zipfile.ZipFile(OUTPUT_WGT, 'w', zipfile.ZIP_DEFLATED) as z:
        for full_path, arc_name in files_to_pack:
            z.write(full_path, arc_name)

    size_kb = round(os.path.getsize(OUTPUT_WGT) / 1024, 1)
    print(f"✅ Pacote gerado com sucesso: {OUTPUT_WGT} ({size_kb} KB)")
    print("-" * 68)
    return True

def list_connected_devices():
    if not os.path.exists(SDB_BIN):
        return []
    try:
        out = subprocess.check_output([SDB_BIN, "devices"], text=True, errors="ignore")
        lines = [line.strip() for line in out.strip().split("\n") if line.strip() and not line.startswith("*") and not line.startswith("List")]
        return lines
    except Exception as e:
        print(f"Erro ao consultar dispositivos via SDB: {e}")
        return []

def connect_to_tv(tv_ip):
    if not os.path.exists(SDB_BIN):
        print("❌ SDB não encontrado!")
        return False
    clean_ip = tv_ip.replace("http://", "").replace(":26101", "").strip()
    target = f"{clean_ip}:26101"
    print(f"📡 Conectando à Smart TV Samsung em {target}...")
    try:
        res = subprocess.run([SDB_BIN, "connect", target], capture_output=True, text=True, timeout=12)
        output = (res.stdout + res.stderr).strip()
        print(f"   ↳ Resposta: {output}")
        if "connected" in output.lower():
            print("✅ Conectado com sucesso à TV!")
            return True
        else:
            print("⚠️ A TV não aceitou a conexão imediata.")
            print("   Certifique-se de que o Developer Mode está ativado na TV e que colocou o IP do PC nela!")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def install_on_tv(tv_ip=None):
    package_wgt()

    devices = list_connected_devices()
    if tv_ip:
        connect_to_tv(tv_ip)
        devices = list_connected_devices()

    if not devices:
        print("⚠️ Nenhuma TV conectada no momento via SDB.")
        print(f"👉 Para conectar, execute: python build_tizen.py --connect <IP_DA_TV>")
        return False

    serial = devices[0].split()[0]
    print(f"📺 Dispositivo detectado: {serial}")
    print(f"🚀 Instalando {OUTPUT_WGT} na Smart TV Samsung...")

    if os.path.exists(TZ_BIN):
        cmd = [TZ_BIN, "install", "-p", OUTPUT_WGT, "-e", serial]
    else:
        cmd = [SDB_BIN, "install", OUTPUT_WGT]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore", timeout=60)
        output = (res.stdout + res.stderr).strip()
        print(f"   ↳ Log da instalação:\n{output}")
        if "completed" in output.lower() or "success" in output.lower():
            print("🎉 CineLocal instalado com sucesso na sua Smart TV Samsung!")
            run_on_tv(serial)
            return True
        else:
            print("⚠️ A TV retornou resposta inesperada durante a instalação.")
            return False
    except Exception as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def run_on_tv(serial=None):
    if not serial:
        devices = list_connected_devices()
        if not devices:
            print("❌ Nenhuma TV conectada para executar o app.")
            return False
        serial = devices[0].split()[0]

    print(f"▶️ Executando {PACKAGE_ID} na TV ({serial})...")
    if os.path.exists(TZ_BIN):
        res = subprocess.run([TZ_BIN, "run", "-p", PACKAGE_ID, "-e", serial], capture_output=True, text=True, errors="ignore")
        out = (res.stdout + res.stderr).strip()
        print(f"   ↳ {out}")
        return "successfully" in out.lower()
    return False

def open_certificate_manager():
    if os.path.exists(CERT_MGR_BIN):
        print("🔑 Abrindo Gerenciador de Certificados Samsung...")
        subprocess.Popen([CERT_MGR_BIN])
    else:
        print("❌ Certificate Manager não encontrado.")

def open_device_manager():
    if os.path.exists(DEV_MGR_BIN):
        print("🖥️ Abrindo Gerenciador de Dispositivos Samsung (Device Manager)...")
        subprocess.Popen([DEV_MGR_BIN])
    else:
        print("❌ Device Manager não encontrado.")

def scan_local_subnet():
    pc_ip = get_local_pc_ip()
    prefix = ".".join(pc_ip.split(".")[:3])
    print(f"🔎 Varrendo a rede local ({prefix}.1 a {prefix}.254) procurando Smart TVs...")
    import concurrent.futures

    found = []
    def check_ip(ip):
        for p in (26101, 8001, 8002):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.35)
            try:
                if s.connect_ex((ip, p)) == 0:
                    return (ip, p)
            except Exception:
                pass
            finally:
                s.close()
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_ip, f"{prefix}.{i}") for i in range(1, 255)]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            if res:
                found.append(res)
                print(f"   ↳ [ENCONTRADO] IP: {res[0]} (Porta {res[1]})")

    if not found:
        print("Nenhuma TV com portas abertas respondeu na varredura rápida.")
    else:
        print(f"✅ {len(found)} dispositivo(s) encontrado(s)!")
    return found

def main():
    banner()
    check_sdk_status()

    parser = argparse.ArgumentParser(description="Gerenciador CineLocal para Samsung Smart TV (Tizen OS)")
    parser.add_argument("--build", action="store_true", help="Gera o pacote dist/CineLocal.wgt assinado")
    parser.add_argument("--connect", type=str, help="Conecta à Smart TV via SDB usando o IP fornecido")
    parser.add_argument("--install", type=str, nargs="?", const="auto", help="Instala o pacote CineLocal.wgt na TV (opcional: passe o IP)")
    parser.add_argument("--run", action="store_true", help="Abre o aplicativo CineLocal diretamente na tela da TV")
    parser.add_argument("--cert", action="store_true", help="Abre a interface gráfica do Certificate Manager")
    parser.add_argument("--device-manager", action="store_true", help="Abre a interface gráfica do Device Manager")
    parser.add_argument("--scan", action="store_true", help="Efetua varredura na rede local procurando a Smart TV")
    
    args = parser.parse_args()

    if args.cert:
        open_certificate_manager()
        return

    if args.device_manager:
        open_device_manager()
        return

    if args.scan:
        scan_local_subnet()
        return

    if args.connect:
        package_wgt()
        connect_to_tv(args.connect)
        return

    if args.install:
        ip = None if args.install == "auto" else args.install
        install_on_tv(ip)
        return

    if args.run:
        run_on_tv()
        return

    package_wgt()
    devices = list_connected_devices()
    print("📋 STATUS ATUAL:")
    if devices:
        print(f"   🟢 TV Conectada: {devices}")
        print("   Para instalar agora, execute: python build_tizen.py --install")
        print("   Para abrir na TV, execute:    python build_tizen.py --run")
    else:
        print("   ⚪ Nenhuma TV conectada no momento via SDB.")
        print(f"   1. Ative o Developer Mode na TV (Apps -> 12345 -> Host PC IP: {get_local_pc_ip()})")
        print("   2. Conecte pelo terminal: python build_tizen.py --connect <IP_DA_TV>")
        print("   3. Ou abra a interface visual: python build_tizen.py --device-manager")
    print("=" * 68)

if __name__ == "__main__":
    main()
