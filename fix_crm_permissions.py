#!/usr/bin/env python3
# Script para dar permisos de CRM al usuario admin

import xmlrpc.client

# Configuración
url = 'http://localhost:8069'
db = 'odoo_test'
username = 'admin'
password = 'admin'

# Conectar a Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"✅ Conectado como usuario ID: {uid}")
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Buscar grupos de Sales/CRM
    sales_groups = models.execute_kw(db, uid, password,
        'res.groups', 'search_read',
        [[['category_id.name', '=', 'Sales']]],
        {'fields': ['name', 'id']})
    
    print(f"\n📊 Grupos de Sales encontrados:")
    for group in sales_groups:
        print(f"  - {group['name']} (ID: {group['id']})")
    
    # Buscar el grupo de Administrator
    admin_group = [g for g in sales_groups if 'Administrator' in g['name']]
    
    if admin_group:
        group_id = admin_group[0]['id']
        print(f"\n🔧 Agregando grupo 'Sales / Administrator' (ID: {group_id}) al usuario admin...")
        
        # Agregar el grupo al usuario
        models.execute_kw(db, uid, password,
            'res.users', 'write',
            [[uid], {'groups_id': [(4, group_id)]}])
        
        print("✅ Permisos de CRM agregados exitosamente!")
        print("\n📋 Ahora puedes:")
        print("  1. Recargar la página en el navegador (F5)")
        print("  2. Ir a CRM desde el menú de aplicaciones")
        print("  3. Ver todos los leads creados")
    else:
        print("❌ No se encontró el grupo de Sales Administrator")
else:
    print("❌ Error al conectar con Odoo")
