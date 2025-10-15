# ✅ Solución: Ver Leads de Cuba en Odoo

## 🎯 Problema

Los leads de Henry Desouza están en la compañía **Cuba**, pero en la interfaz de Odoo solo ves **USA**.

---

## ✅ Verificación en Base de Datos

Los leads **SÍ están en Cuba**:

```sql
SELECT l.id, l.contact_name, l.phone, l.type, c.name as company 
FROM crm_lead l 
JOIN res_company c ON l.company_id = c.id 
WHERE l.contact_name ILIKE '%desouza%';
```

**Resultado:**
```
 id |       contact_name        |    phone    | type | company 
----+---------------------------+-------------+------+---------
 45 | Hurshel DeSouza Noguera   | 053065305   | lead | Cuba ✅
 46 | Hurshelll DeSouza Noguera | 053065305   | lead | Cuba ✅
 51 | Henry Desouza Noguera     | +5353065301 | lead | Cuba ✅
```

---

## 🔍 ¿Por qué no los ves en Odoo?

Odoo filtra los registros por la **compañía activa** del usuario. Si tu usuario está viendo solo la compañía USA, no verás los leads de Cuba.

---

## 🔧 Solución: Cambiar Compañía en Odoo

### Opción 1: Cambiar Compañía Activa (Recomendado)

1. **En la esquina superior derecha** de Odoo, verás el nombre de tu usuario
2. Click en tu nombre de usuario
3. Verás un selector de compañías
4. **Selecciona "Cuba"** (o marca todas las compañías)
5. Refresca la página (F5)

Ahora deberías ver los leads de Cuba.

### Opción 2: Ver Todas las Compañías

1. Click en tu nombre de usuario (esquina superior derecha)
2. En el selector de compañías, **marca todas**:
   - ☑ YourCompany
   - ☑ Colombia
   - ☑ México
   - ☑ USA
   - ☑ **Cuba** ← Importante
3. Refresca la página

### Opción 3: Filtrar por Compañía en CRM

1. Ve a **CRM → Leads**
2. En la barra de búsqueda, click en **"Filtros"**
3. Agregar filtro personalizado:
   - Campo: **Compañía**
   - Operador: **es igual a**
   - Valor: **Cuba**
4. Aplicar filtro

---

## 🎯 Dar Acceso a Cuba al Usuario Admin

Si el usuario admin no tiene acceso a la compañía Cuba, necesitas agregarlo:

### Desde la Interfaz:

1. **Configuración → Usuarios y Compañías → Usuarios**
2. Buscar tu usuario (admin)
3. Click en tu usuario
4. En la pestaña **"Compañías Permitidas"**
5. Agregar **Cuba**
6. Guardar

### Desde Script (Más Rápido):

Ejecuta este script:

```python
# Dar acceso a Cuba al usuario admin
admin = env['res.users'].search([('login', '=', 'admin')], limit=1)
cuba = env['res.company'].search([('name', '=', 'Cuba')], limit=1)

if admin and cuba:
    if cuba.id not in admin.company_ids.ids:
        admin.write({'company_ids': [(4, cuba.id)]})
        print(f"✅ Compañía Cuba agregada al usuario admin")
    else:
        print(f"✅ Usuario admin ya tiene acceso a Cuba")
    
    env.cr.commit()
```

---

## 📊 Compañías Disponibles

```
 id |    name     
----+-------------
  1 | YourCompany
  2 | Colombia
  3 | México
  4 | USA
  8 | Cuba        ← Nueva
```

---

## 🧪 Verificar Acceso del Usuario

Para verificar a qué compañías tiene acceso tu usuario:

```sql
SELECT u.login, c.name as company
FROM res_users u
JOIN res_company_users_rel r ON u.id = r.user_id
JOIN res_company c ON r.cid = c.id
WHERE u.login = 'admin'
ORDER BY c.name;
```

---

## 🎯 Pasos para Ver los Leads de Cuba

### Paso 1: Verificar Acceso
```bash
# Ejecutar script para dar acceso
docker exec odoo18_web bash -c "odoo shell -d odoo_test --config=/etc/odoo/odoo.conf --no-http" << 'EOF'
admin = env['res.users'].search([('login', '=', 'admin')], limit=1)
cuba = env['res.company'].search([('name', '=', 'Cuba')], limit=1)
if admin and cuba and cuba.id not in admin.company_ids.ids:
    admin.write({'company_ids': [(4, cuba.id)]})
    env.cr.commit()
    print("✅ Acceso agregado")
else:
    print("✅ Ya tiene acceso")
EOF
```

### Paso 2: En Odoo
1. Recargar la página (F5)
2. Click en tu nombre (esquina superior derecha)
3. Seleccionar compañía **Cuba**
4. Ir a **CRM → Leads**
5. Deberías ver los 3 leads de DeSouza

---

## 📋 Leads de Cuba

Una vez que cambies a la compañía Cuba, verás:

| ID | Nombre | Teléfono | Email | Equipo |
|----|--------|----------|-------|--------|
| 45 | Hurshel DeSouza Noguera | 053065305 | - | Website Cuba |
| 46 | Hurshelll DeSouza Noguera | 053065305 | - | Website Cuba |
| 51 | Henry Desouza Noguera | +5353065301 | henrydesouza2025@gmail.com | Website Cuba |

---

## 🔍 Troubleshooting

### Problema: No veo el selector de compañías

**Solución:** Tu usuario necesita acceso a múltiples compañías.

1. Ve a **Configuración → Usuarios**
2. Edita tu usuario
3. En **"Compañías Permitidas"**, agrega Cuba
4. Guarda y recarga

### Problema: Veo Cuba pero no los leads

**Solución:** Verifica que estés en la compañía correcta.

1. Mira la esquina superior derecha
2. Debe decir **"Cuba"** o **"YourCompany, Colombia, México, USA, Cuba"**
3. Si no, cambia la compañía activa

### Problema: Los leads siguen sin aparecer

**Solución:** Verifica los filtros activos.

1. En CRM → Leads
2. Mira si hay filtros activos (arriba de la lista)
3. Quita todos los filtros
4. O agrega filtro: Compañía = Cuba

---

## ✅ Resumen

**Estado actual:**
- ✅ Compañía Cuba creada (ID: 8)
- ✅ Equipo Website Cuba creado (ID: 13)
- ✅ 3 leads asignados a Cuba
- ✅ Detección automática funciona (+53)

**Para ver los leads:**
1. Dar acceso a Cuba al usuario admin
2. Cambiar compañía activa a Cuba
3. Ir a CRM → Leads
4. Ver los 3 leads de DeSouza

---

## 🚀 Script Rápido para Dar Acceso

Copia y pega esto en tu terminal:

```bash
docker exec odoo18_web bash -c "cat > /tmp/give_cuba_access.py << 'SCRIPT'
admin = env['res.users'].search([('login', '=', 'admin')], limit=1)
cuba = env['res.company'].search([('name', '=', 'Cuba')], limit=1)

if not admin:
    print('❌ Usuario admin no encontrado')
    exit()

if not cuba:
    print('❌ Compañía Cuba no encontrada')
    exit()

print(f'Usuario: {admin.login}')
print(f'Compañías actuales: {[c.name for c in admin.company_ids]}')

if cuba.id not in admin.company_ids.ids:
    admin.write({'company_ids': [(4, cuba.id)]})
    env.cr.commit()
    print(f'✅ Compañía Cuba agregada')
else:
    print(f'✅ Ya tiene acceso a Cuba')

print(f'Compañías finales: {[c.name for c in admin.company_ids]}')
SCRIPT
odoo shell -d odoo_test --config=/etc/odoo/odoo.conf --no-http < /tmp/give_cuba_access.py"
```

---

**Fecha:** 15/10/2025
**Compañía Cuba ID:** 8
**Equipo Cuba ID:** 13
**Leads en Cuba:** 3
**Estado:** ✅ Creado y Verificado
