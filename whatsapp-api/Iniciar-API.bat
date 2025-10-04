@echo off
echo ========================================
echo   INICIANDO API DE WHATSAPP
echo ========================================
echo.
echo Verificando Node.js...
node --version
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Descargalo de: https://nodejs.org/
    pause
    exit
)
echo.
echo Instalando dependencias...
call npm install
echo.
echo ========================================
echo   API INICIADA
echo ========================================
echo.
echo IMPORTANTE:
echo - Escanea el codigo QR con WhatsApp
echo - NO CIERRES esta ventana
echo - La API debe estar siempre corriendo
echo.
echo ========================================
npm run api
pause
