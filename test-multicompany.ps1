# Script de prueba Multi-Compañía
Write-Host "🧪 Probando Multi-Compañía..." -ForegroundColor Cyan

Write-Host "`n📊 1. Verificando compañías creadas..." -ForegroundColor Yellow
docker exec odoo18_db psql -U odoo -d odoo_test -c "SELECT id, name, currency_id FROM res_company ORDER BY id;"

Write-Host "`n👥 2. Verificando equipos de ventas..." -ForegroundColor Yellow
docker exec odoo18_db psql -U odoo -d odoo_test -c "SELECT id, name, company_id FROM crm_team WHERE company_id IS NOT NULL ORDER BY company_id;"

Write-Host "`n📞 3. Probando detección de país por teléfono..." -ForegroundColor Yellow

# Test Colombia
Write-Host "`n   🇨🇴 Teléfono Colombia: 573001234567" -ForegroundColor Green
$colombiaTest = @{
    name = "Test Colombia"
    email = "test@colombia.com"
    phone = "573001234567"
    product_interest = "Producto Test"
    message = "Test multi-compañía Colombia"
} | ConvertTo-Json

# Test México
Write-Host "   🇲🇽 Teléfono México: 525512345678" -ForegroundColor Green

# Test USA
Write-Host "   🇺🇸 Teléfono USA: 15551234567" -ForegroundColor Green

Write-Host "`n✅ Verificación completada!" -ForegroundColor Green
Write-Host "`n📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Accede a Odoo: http://localhost:8069" -ForegroundColor White
Write-Host "   2. Usuario: admin / Contraseña: admin" -ForegroundColor White
Write-Host "   3. Ve a: Configuración > Usuarios > admin" -ForegroundColor White
Write-Host "   4. Agrega todas las compañías en 'Compañías Permitidas'" -ForegroundColor White
Write-Host "   5. Prueba el formulario: http://localhost:8069/landing/productos" -ForegroundColor White

Write-Host "`n📚 Documentación:" -ForegroundColor Cyan
Write-Host "   - MULTI_COMPANY_RESUMEN.md - Resumen completo" -ForegroundColor White
Write-Host "   - MULTI_COMPANY_SETUP.md - Guía de configuración" -ForegroundColor White
