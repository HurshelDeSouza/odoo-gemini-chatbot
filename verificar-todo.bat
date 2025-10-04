@echo off
echo ========================================
echo   VERIFICACION COMPLETA DEL SISTEMA
echo ========================================
echo.

echo [1/5] Verificando Docker...
docker ps | findstr odoo18
if errorlevel 1 (
    echo ❌ Odoo no esta corriendo
    echo    Ejecuta: docker-compose up -d
) else (
    echo ✅ Odoo esta corriendo
)
echo.

echo [2/5] Verificando API de WhatsApp...
curl -s http://localhost:3000/status > nul 2>&1
if errorlevel 1 (
    echo ❌ API no esta corriendo
    echo    Ejecuta: cd whatsapp-api ^& Iniciar-API.bat
) else (
    echo ✅ API esta corriendo
    echo    Estado:
    curl -s http://localhost:3000/status
)
echo.

echo [3/5] Verificando archivo CSV...
if exist contactos_cuba_prueba.csv (
    echo ✅ Archivo CSV encontrado
    echo    Contenido:
    type contactos_cuba_prueba.csv
) else (
    echo ❌ Archivo CSV no encontrado
)
echo.

echo [4/5] Verificando estructura de archivos...
if exist whatsapp-api\server.js (
    echo ✅ API: server.js
) else (
    echo ❌ API: server.js no encontrado
)

if exist custom_addons\gemini_chatbot\services\whatsapp_service.py (
    echo ✅ Odoo: whatsapp_service.py
) else (
    echo ❌ Odoo: whatsapp_service.py no encontrado
)
echo.

echo [5/5] URLs importantes...
echo ✅ Odoo: http://localhost:8069
echo ✅ API Status: http://localhost:3000/status
echo.

echo ========================================
echo   RESUMEN
echo ========================================
echo.
echo Si todo esta ✅, puedes enviar mensajes!
echo.
echo Pasos siguientes:
echo 1. Abre: http://localhost:8069
echo 2. Ve a: Gemini Chatbot ^> Campañas WhatsApp
echo 3. Crea una campaña
echo 4. Sube: contactos_cuba_prueba.csv
echo 5. Envia mensajes
echo.
echo ========================================
pause
