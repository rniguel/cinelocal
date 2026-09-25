@echo off
title CineLocal - Atualizar Catalogo
chcp 65001 > nul
cd /d "%~dp0"
echo =======================================================
echo          Atualizando Catalogo de Filmes
echo =======================================================
echo.
python atualizar_catalogo.py
echo.
echo Concluido com sucesso!
pause
