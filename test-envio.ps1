# Script de prueba para enviar mensaje directo
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PRUEBA DE ENVÍO DIRECTO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Verificando API..." -ForegroundColor Yellow
try {
    $status = Invoke-RestMethod -Uri "http://localhost:3000/status" -Method Get
    Write-Host "✅ API Status: $($status.status)" -ForegroundColor Green
    Write-Host "   Mensaje: $($status.message)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al conectar con la API" -ForegroundColor Red
    Write-Host "   Asegúrate de que Iniciar-API.bat esté corriendo" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Enviando mensaje..." -ForegroundColor Yellow
Write-Host "   Número: 5353065305" -ForegroundColor White
Write-Host "   Mensaje: sevende macbookpro" -ForegroundColor White
Write-Host ""

try {
    $body = @{
        phone = "5353065305"
        message = "sevende macbookpro"
    } | ConvertTo-Json

    $result = Invoke-RestMethod -Uri "http://localhost:3000/send-message" -Method Post -Body $body -ContentType "application/json"
    
    if ($result.success) {
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "   ✅ MENSAJE ENVIADO EXITOSAMENTE" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Detalles:" -ForegroundColor Cyan
        Write-Host "   Número: $($result.phone)" -ForegroundColor White
        Write-Host "   Estado: $($result.message)" -ForegroundColor White
        Write-Host ""
        Write-Host "El mensaje 'sevende macbookpro' fue enviado a +53 53065305" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al enviar mensaje" -ForegroundColor Red
        Write-Host "   Error: $($result.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error en la solicitud" -ForegroundColor Red
    Write-Host "   Detalles: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
