@echo off
chcp 65001 >nul
color 0B
cls

echo ========================================
echo VENDEXA - Instalação Automática
echo ========================================
echo.
echo Este script irá:
echo 1. Verificar Python
echo 2. Instalar dependências
echo 3. Configurar banco de dados
echo 4. Preparar o sistema
echo.
pause
echo.

python setup.py

if errorlevel 1 (
    echo.
    echo ERRO: Instalação falhou
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalação concluída com sucesso!
echo ========================================
echo.
echo Para iniciar o sistema, execute:
echo START.bat
echo.
echo ou digite:
echo python main.py
echo.
pause
