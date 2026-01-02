@echo off
chcp 65001 >nul
color 0A
cls

echo ========================================
echo VENDEXA - Sistema de Vendas Autônomo
echo ========================================
echo.
echo Iniciando sistema...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao iniciar o sistema
    echo.
    echo Verifique se:
    echo 1. Python está instalado
    echo 2. Dependências foram instaladas (pip install -r requirements.txt)
    echo 3. Arquivos de configuração estão corretos
    echo.
    pause
)
