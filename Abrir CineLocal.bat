@echo off
title CineLocal Desktop
chcp 65001 > nul
cd /d "%~dp0"

echo =======================================================
echo          Iniciando CineLocal Desktop
echo =======================================================
echo.
python run_desktop.py
if errorlevel 1 (
    cd /d "%~dp0app"
    python servidor.py --browser
)
