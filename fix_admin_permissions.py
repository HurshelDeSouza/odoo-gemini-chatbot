#!/usr/bin/env python3
# Script para dar permisos completos de administración al usuario admin

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
    print(f"✅ Conectado como usuario ID: {uid}\n")
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Grupos críticos que debe tener el admin
    critical_groups = [
        'base.group_system',           # Administration / Settings
        'base.group_erp_manager',      # Administration / Access Rights
        'sales_team.group_sale_manager',  # Sales / Manager
    ]
    
    print("🔧 Agregando grupos críticos al usuario admin...\n")
    
    for group_xmlid in critical_groups:
        try:
            # Buscar el grupo
            group = models.execute_kw(db, uid, password,
                'ir.model.data', 'search_read',
                [[['name', '=', group_xmlid.split('.')[1]], ['module', '=', group_xmlid.split('.')[0]]]],
                {'fields': ['res_id'], 'limit': 1})
            
            if group:
                group_id = group[0]['res_id']
                
                # Agregar el grupo al usuario
                models.execute_kw(db, uid, password,
                    'res.users', 'write',
                    [[uid], {'groups_id': [(4, group_id)]}])
                
                print(f"  ✅ Agregado: {group_xmlid}")
            else:
                print(f"  ⚠️  No encontrado: {group_xmlid}")
        except Exception as e:
            print(f"  ❌ Error con {group_xmlid}: {e}")
    
    print("\n✅ Permisos de administración agregados exitosamente!")
    print("\n📋 Ahora puedes:")
    print("  1. Recargar la página en el navegador (F5)")
    print("  2. Acceder a Configuración")
    print("  3. Gestionar usuarios y permisos")
    print("  4. Acceder a todas las funcionalidades\n")
else:
    print("❌ Error al conectar con Odoo")
