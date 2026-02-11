@echo off
echo ========================================
echo  Verificador de MKVToolNix
echo ========================================
echo.

REM Verificar si mkvmerge está instalado
where mkvmerge >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] MKVToolNix ya esta instalado
    mkvmerge --version
    echo.
    echo Todo listo para trabajar con archivos MKV!
    pause
    exit /b 0
)

echo [!] MKVToolNix NO esta instalado
echo.
echo MKVToolNix es necesario para:
echo - Extraer subtitulos de archivos MKV
echo - Insertar subtitulos en archivos MKV
echo - Manipular pistas de video
echo.
echo ========================================
echo  INSTALACION AUTOMATICA
echo ========================================
echo.

set /p install="Deseas descargar e instalar MKVToolNix ahora? (S/N): "
if /i "%install%" NEQ "S" (
    echo.
    echo Instalacion cancelada.
    echo.
    echo Puedes descargarlo manualmente desde:
    echo https://mkvtoolnix.download/downloads.html
    echo.
    pause
    exit /b 1
)

echo.
echo Abriendo pagina de descarga...
echo.
start https://mkvtoolnix.download/downloads.html#windows

echo.
echo ========================================
echo  INSTRUCCIONES:
echo ========================================
echo 1. Descarga "MKVToolNix installer"
echo 2. Ejecuta el instalador
echo 3. IMPORTANTE: Durante la instalacion marca:
echo    [X] Add mkvtoolnix to PATH
echo 4. Completa la instalacion
echo 5. Vuelve a ejecutar este archivo para verificar
echo ========================================
echo.
pause
