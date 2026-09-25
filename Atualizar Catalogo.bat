@echo off
title CineLocal - Atualizar Catalogo
chcp 65001 > nul
cd /d "%~dp0"
echo =======================================================
echo          CineLocal - Atualizando Catalogo
echo =======================================================
echo.
python app\atualizar_catalogo.py
echo.
echo Concluido com sucesso!
pause
