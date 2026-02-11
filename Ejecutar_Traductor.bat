@echo off
title DeepL Subtitle Translator v2.0
cls

echo ========================================
echo   DeepL Subtitle Translator v2.0
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

REM Verificar si las dependencias están instaladas
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias necesarias...
    echo.
    call instalar.bat
)

REM Ejecutar la aplicación
echo Iniciando aplicacion...
echo.
python subtitle_translator_gui_v2.py

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema al ejecutar la aplicacion
    echo.
    pause
)
