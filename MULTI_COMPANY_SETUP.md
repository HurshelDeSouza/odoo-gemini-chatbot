# 🏢 Configuración Multi-Compañía

## 📋 Compañías Creadas

Este módulo crea automáticamente 3 compañías:

1. **🇨🇴 Colombia**
   - Moneda: COP (Peso Colombiano)
   - Código telefónico: +57
   - Equipos: "Ventas Colombia" y "Website Colombia"

2. **🇲🇽 México**
   - Moneda: MXN (Peso Mexicano)
   - Código telefónico: +52
   - Equipos: "Ventas México" y "Website México"

3. **🇺🇸 USA**
   - Moneda: USD (Dólar)
   - Código telefónico: +1
   - Equipos: "Ventas USA" y "Website USA"

---

## 🚀 Instalación

### 1. Actualizar el módulo

```bash
docker exec odoo18_web odoo -d odoo_test -u landing_page_productos --stop-after-init
```

### 2. Reiniciar Odoo

```bash
docker-compose restart
```

### 3. Activar Multi-Compañía en Odoo

1. Ir a: **Configuración > Usuarios y Compañías > Usuarios**
2. Editar el usuario **admin**
3. En la pestaña **Compañías Permitidas**, seleccionar todas las compañías:
   - ✅ YourCompany
   - ✅ Colombia
   - ✅ México
   - ✅ USA
4. Guardar

---

## 🎯 Cómo Funciona

### Detección Automática por Teléfono

Cuando un lead llena el formulario, el sistema detecta automáticamente la compañía según el código de país:

```
Teléfono: 573001234567 → Compañía: Colombia
Teléfono: 525512345678 → Compañía: México
Teléfono: 15551234567  → Compañía: USA
```

### Asignación de Equipos

Cada lead se asigna automáticamente al equipo "Website" de su compañía:

```
Lead de Colombia → Equipo "Website Colombia"
Lead de México   → Equipo "Website México"
Lead de USA      → Equipo "Website USA"
```

---

## 👥 Configuración de Usuarios

### Crear usuarios por compañía

1. **Usuario Colombia:**
   - Ir a: Configuración > Usuarios
   - Crear nuevo usuario
   - Compañía: Colombia
   - Equipos de ventas: Ventas Colombia, Website Colombia

2. **Usuario México:**
   - Compañía: México
   - Equipos de ventas: Ventas México, Website México

3. **Usuario USA:**
   - Compañía: USA
   - Equipos de ventas: Ventas USA, Website USA

---

## 📊 Reportes por Compañía

### Ver leads por compañía

1. Ir a: **CRM > Leads**
2. Filtrar por compañía en la barra superior
3. Cambiar entre compañías con el selector

### Reportes de ventas

1. Ir a: **CRM > Reportes > Pipeline**
2. Agrupar por: Compañía
3. Ver métricas separadas por país

---

## 🔧 Personalización

### Agregar más compañías

Editar: `custom_addons/landing_page_productos/data/company_data.xml`

```xml
<record id="company_spain" model="res.company">
    <field name="name">España</field>
    <field name="currency_id" ref="base.EUR"/>
    <field name="country_id" ref="base.es"/>
    <field name="email">info@spain.example.com</field>
    <field name="phone">+34 91 123 4567</field>
</record>
```

### Agregar detección de país

Editar: `custom_addons/landing_page_productos/controllers/main.py`

```python
elif clean_phone.startswith('34'):  # España
    company = request.env['res.company'].sudo().search([('name', '=', 'España')], limit=1)
    return company.id if company else request.env.company.id
```

---

## ✅ Verificación

### Comprobar que funciona:

1. **Ver compañías creadas:**
   - Configuración > Usuarios y Compañías > Compañías
   - Deberías ver: YourCompany, Colombia, México, USA

2. **Ver equipos de ventas:**
   - CRM > Configuración > Equipos de Ventas
   - Deberías ver 6 equipos nuevos (2 por compañía)

3. **Probar el formulario:**
   - Ir a: http://localhost:8069/landing/productos
   - Llenar con teléfono colombiano: 573001234567
   - Verificar en CRM que el lead tiene compañía "Colombia"

---

## 🐛 Troubleshooting

### Los leads no tienen compañía asignada

**Solución:**
- Verificar que el teléfono tenga el código de país
- Verificar que las compañías existan en el sistema

### No veo las compañías en el selector

**Solución:**
- Ir a Configuración > Usuarios
- Editar tu usuario
- Agregar todas las compañías en "Compañías Permitidas"

### Los equipos no aparecen

**Solución:**
```bash
docker exec odoo18_web odoo -d odoo_test -u landing_page_productos --stop-after-init
docker-compose restart
```

---

## 📞 Códigos de País Soportados

| País     | Código | Ejemplo          |
|----------|--------|------------------|
| Colombia | +57    | 573001234567     |
| México   | +52    | 525512345678     |
| USA      | +1     | 15551234567      |

---

## 🎓 Recursos

- [Documentación Odoo Multi-Company](https://www.odoo.com/documentation/18.0/applications/general/companies.html)
- [CRM Multi-Company](https://www.odoo.com/documentation/18.0/applications/sales/crm.html)
