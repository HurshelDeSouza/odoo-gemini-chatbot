# Script para verificar campañas y mostrar URLs de landing pages
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VERIFICAR CAMPAÑAS Y LANDING PAGES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Verificando Odoo..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8069" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Odoo está corriendo" -ForegroundColor Green
} catch {
    Write-Host "❌ Odoo no está corriendo" -ForegroundColor Red
    Write-Host "   Ejecuta: docker-compose up -d" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   LANDING PAGES DISPONIBLES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Probando URLs de landing pages..." -ForegroundColor Yellow
Write-Host ""

$found = $false

for ($i = 1; $i -le 5; $i++) {
    $url = "http://localhost:8069/product/landing/$i"
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Campaña $i encontrada:" -ForegroundColor Green
            Write-Host "   URL: $url" -ForegroundColor White
            Write-Host ""
            $found = $true
        }
    } catch {
        # Silenciosamente continuar
    }
}

if (-not $found) {
    Write-Host "❌ No se encontraron campañas" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCIÓN:" -ForegroundColor Yellow
    Write-Host "1. Abre Odoo: http://localhost:8069" -ForegroundColor White
    Write-Host "2. Ve a: Gemini Chatbot > Campañas WhatsApp" -ForegroundColor White
    Write-Host "3. Crea una nueva campaña" -ForegroundColor White
    Write-Host "4. Después de guardar, copia la URL Landing Page" -ForegroundColor White
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   DIFERENCIA IMPORTANTE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "❌ Landing Page del Chatbot (NO es esta):" -ForegroundColor Red
Write-Host "   http://localhost:8069/chatbot" -ForegroundColor White
Write-Host "   → Tiene robot y chat, NO tiene formulario" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Landing Page de Producto (SÍ es esta):" -ForegroundColor Green
Write-Host "   http://localhost:8069/product/landing/{id}" -ForegroundColor White
Write-Host "   → Tiene formulario de registro" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
