#!/usr/bin/env python3
# Script para configurar todas las compañías al usuario admin

import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo_test'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"✅ Conectado como usuario ID: {uid}\n")
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Obtener todas las compañías
    companies = models.execute_kw(db, uid, password,
        'res.company', 'search_read',
        [[]],
        {'fields': ['name', 'id', 'currency_id', 'phone']})
    
    print("🏢 Compañías encontradas:\n")
    for company in companies:
        currency = company.get('currency_id', [False, 'N/A'])
        currency_name = currency[1] if currency else 'N/A'
        phone = company.get('phone', 'N/A')
        print(f"  {company['id']}. {company['name']}")
        print(f"     💰 Moneda: {currency_name}")
        print(f"     📞 Teléfono: {phone}\n")
    
    # Obtener IDs de todas las compañías
    company_ids = [c['id'] for c in companies]
    
    print(f"🔧 Agregando todas las compañías al usuario admin...\n")
    
    # Actualizar usuario con todas las compañías
    models.execute_kw(db, uid, password,
        'res.users', 'write',
        [[uid], {'company_ids': [(6, 0, company_ids)]}])
    
    print("✅ Configuración completada!\n")
    print("📋 Ahora puedes:")
    print("  1. Recargar la página (F5)")
    print("  2. Ver el selector de compañías en la esquina superior derecha")
    print("  3. Cambiar entre: YourCompany, Colombia, México, USA")
    print("  4. Ver leads filtrados por compañía\n")
    
else:
    print("❌ Error al conectar con Odoo")
