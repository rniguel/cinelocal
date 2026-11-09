@echo off
title CineLocal Desktop
chcp 65001 >nul
cd /d "%~dp0"

echo ===================================================
echo   🎬 CINELOCAL DESKTOP - INICIANDO APLICATIVO
echo ===================================================

rem Desbloqueia executavel no Windows se necessario
powershell -Command "if (Test-Path 'dist\CineLocal\CineLocal.exe') { Unblock-File 'dist\CineLocal\CineLocal.exe' }" 2>nul

rem 1. Se o Python estiver disponivel, inicia via run_desktop.py
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Iniciando aplicativo CineLocal...
    python run_desktop.py
    goto end
)

rem 2. Fallback: executa o executavel CineLocal.exe compilado
if exist "dist\CineLocal\CineLocal.exe" (
    echo [OK] Iniciando executavel CineLocal.exe...
    start "" "dist\CineLocal\CineLocal.exe"
    goto end
)

echo [ERRO] Python ou dist\CineLocal\CineLocal.exe nao encontrados.
pause

:end
