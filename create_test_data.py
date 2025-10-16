#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear datos de prueba en Odoo
Ejecutar con: docker exec -it odoo18_web python3 /mnt/extra-addons/../create_test_data.py
"""

import xmlrpc.client

# Configuración
url = 'http://localhost:8069'
db = 'odoo_test'
username = 'admin'
password = 'admin'

# Conectar a Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

print(f"Conectado como usuario ID: {uid}")

# Datos de compañías
companies_data = [
    {
        'name': 'Tech Solutions Colombia',
        'country_code': 'CO',
        'phone': '+57 1 234 5678',
        'email': 'info@techsolutions.co',
    },
    {
        'name': 'Innovate Mexico SA',
        'country_code': 'MX',
        'phone': '+52 55 1234 5678',
        'email': 'contacto@innovate.mx',
    },
    {
        'name': 'Digital USA Corp',
        'country_code': 'US',
        'phone': '+1 555 123 4567',
        'email': 'hello@digitalusa.com',
    },
    {
        'name': 'Caribbean Solutions Cuba',
        'country_code': 'CU',
        'phone': '+53 7 123 4567',
        'email': 'info@caribbean.cu',
    },
    {
        'name': 'Global Services Argentina',
        'country_code': 'AR',
        'phone': '+54 11 1234 5678',
        'email': 'contacto@global.ar',
    },
]

# Nombres para leads
lead_names = [
    ['Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Luis Rodríguez'],
    ['José Hernández', 'Laura González', 'Miguel Sánchez', 'Carmen Ramírez', 'Pedro Torres'],
    ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 'David Wilson'],
    ['Roberto Castro', 'Isabel Díaz', 'Fernando Ruiz', 'Patricia Morales', 'Jorge Ortiz'],
    ['Martín Fernández', 'Lucía Silva', 'Diego Romero', 'Valentina Vargas', 'Sebastián Medina'],
]

productos = [
    'Producto Premium A',
    'Producto Estándar B',
    'Producto Deluxe C',
    'Producto Básico D',
    'Producto Especial E',
]

print("\n=== Creando compañías y leads ===\n")

for idx, company_data in enumerate(companies_data):
    # Buscar país
    country_id = models.execute_kw(db, uid, password,
        'res.country', 'search',
        [[['code', '=', company_data['country_code']]]], {'limit': 1})
    
    if not country_id:
        print(f"⚠️  País {company_data['country_code']} no encontrado, usando país por defecto")
        country_id = [1]
    
    # Buscar moneda del país
    country = models.execute_kw(db, uid, password,
        'res.country', 'read',
        [country_id], {'fields': ['currency_id']})
    
    currency_id = country[0]['currency_id'][0] if country[0].get('currency_id') else 1
    
    # Crear compañía
    company_id = models.execute_kw(db, uid, password,
        'res.company', 'create',
        [{
            'name': company_data['name'],
            'country_id': country_id[0],
            'currency_id': currency_id,
            'phone': company_data['phone'],
            'email': company_data['email'],
        }])
    
    print(f"✅ Compañía creada: {company_data['name']} (ID: {company_id})")
    
    # Crear equipo de ventas para esta compañía
    team_id = models.execute_kw(db, uid, password,
        'crm.team', 'create',
        [{
            'name': f'Equipo Ventas {company_data["name"]}',
            'company_id': company_id,
            'use_leads': True,
            'use_opportunities': True,
        }])
    
    print(f"   📊 Equipo de ventas creado (ID: {team_id})")
    
    # Crear 5 leads para esta compañía
    for lead_idx, lead_name in enumerate(lead_names[idx]):
        lead_id = models.execute_kw(db, uid, password,
            'crm.lead', 'create',
            [{
                'name': f'Lead - {lead_name}',
                'contact_name': lead_name,
                'email_from': f'{lead_name.lower().replace(" ", ".")}@example.com',
                'phone': company_data['phone'],
                'company_id': company_id,
                'team_id': team_id,
                'type': 'lead',
                'description': f'Interesado en {productos[lead_idx]}\n\nContacto generado para pruebas.',
            }])
        
        print(f"   👤 Lead creado: {lead_name} (ID: {lead_id})")
    
    print()

print("=== ✅ Datos de prueba creados exitosamente ===")
print(f"\nTotal: {len(companies_data)} compañías con 5 leads cada una = {len(companies_data) * 5} leads")
