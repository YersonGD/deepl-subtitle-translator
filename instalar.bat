@echo off
echo ========================================
echo  Instalador de DeepL Subtitle Translator v2.0
echo ========================================
echo.

echo Instalando dependencias de Python...
echo.

pip install customtkinter
pip install deepl
pip install tkinterdnd2

echo.
echo ========================================
echo  Dependencias de Python instaladas!
echo ========================================
echo.
echo IMPORTANTE: Para usar la funcion MKV necesitas:
echo.
echo 1. Descargar MKVToolNix desde:
echo    https://mkvtoolnix.download/downloads.html
echo.
echo 2. Durante la instalacion, marcar:
echo    [X] Add mkvtoolnix to PATH
echo.
echo Ejecuta 'verificar_mkvtoolnix.bat' para verificar
echo.
pause
