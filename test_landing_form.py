#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el formulario de la landing page
"""

import requests
import json

url = 'http://localhost:8069/landing/submit'

# Datos de prueba para diferentes países
test_leads = [
    {
        'name': 'Andrés Gómez Ruiz',
        'email': 'andres.gomez@test.co',
        'phone': '+573001234567',  # Colombia
        'product_interest': 'Paquete 2 - 2 unidades',
        'message': 'Departamento: Cundinamarca\nCiudad: Bogotá\nDirección: Calle 100 #15-20\nBarrio: Chicó\nTeléfono confirmación: +573001234567\nEnvío prioritario: Sí',
    },
    {
        'name': 'Sofía Martínez López',
        'email': 'sofia.martinez@test.mx',
        'phone': '+525512345678',  # México
        'product_interest': 'Paquete 3 - 3 unidades',
        'message': 'Departamento: Ciudad de México\nCiudad: CDMX\nDirección: Av. Reforma 123\nBarrio: Polanco\nTeléfono confirmación: +525512345678\nEnvío prioritario: No',
    },
    {
        'name': 'Robert Anderson',
        'email': 'robert.anderson@test.com',
        'phone': '+15551234567',  # USA
        'product_interest': 'Paquete 1 - 1 unidad',
        'message': 'Departamento: California\nCiudad: Los Angeles\nDirección: 123 Main St\nBarrio: Downtown\nTeléfono confirmación: +15551234567\nEnvío prioritario: Sí',
    },
    {
        'name': 'Camila Rodríguez',
        'email': 'camila.rodriguez@test.cu',
        'phone': '+5371234567',  # Cuba
        'product_interest': 'Paquete 2 - 2 unidades',
        'message': 'Departamento: La Habana\nCiudad: Habana\nDirección: Calle 23 #456\nBarrio: Vedado\nTeléfono confirmación: +5371234567\nEnvío prioritario: No',
    },
]

print("\n=== Probando formulario de Landing Page ===\n")

for idx, lead_data in enumerate(test_leads, 1):
    print(f"📝 Enviando lead {idx}/4: {lead_data['name']} ({lead_data['phone']})")
    
    # Preparar payload JSON-RPC
    payload = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': lead_data,
        'id': idx
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('result', {}).get('success'):
                lead_id = result['result'].get('lead_id')
                print(f"   ✅ Lead creado exitosamente (ID: {lead_id})")
                print(f"   📧 Email: {lead_data['email']}")
                print(f"   📱 Teléfono: {lead_data['phone']}")
            else:
                message = result.get('result', {}).get('message', 'Error desconocido')
                print(f"   ❌ Error: {message}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
    
    print()

print("=== ✅ Pruebas completadas ===")
print("\nVerifica en Odoo:")
print("1. Ve a CRM → Leads")
print("2. Deberías ver los nuevos leads creados desde la landing page")
print("3. Verifica que cada lead esté asignado a la compañía correcta según el código de país")
