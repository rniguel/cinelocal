@echo off
title CineLocal - Servidor de Streaming
chcp 65001 > nul
cd /d "%~dp0"
echo =======================================================
echo          Iniciando CineLocal Home Theater
echo =======================================================
echo.
python servidor.py
pause
