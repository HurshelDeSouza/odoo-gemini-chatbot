# 📱 CÓMO ACCEDER A LA LANDING PAGE DE REGISTRO

## ❌ PROBLEMA

Estás viendo la landing page del **Chatbot** (la que tiene el robot y subir archivos).

Esa NO es la landing page para capturar leads.

---

## ✅ SOLUCIÓN

Necesitas acceder a la **Landing Page de Producto** que tiene el formulario de registro.

---

## 🚀 PASOS PARA ACCEDER

### PASO 1: Crear o Abrir una Campaña

1. Abre Odoo: `http://localhost:8069`
2. Ve a: **Gemini Chatbot > Campañas WhatsApp**
3. Si no tienes campañas, crea una:
   - Clic en **Crear**
   - Nombre: "Prueba Landing Page"
   - Producto: "MacBook Pro"
   - Descripción: "MacBook Pro en venta"
   - Sube cualquier CSV (o usa `contacto_macbook.csv`)
   - Mensaje: "Hola"
   - **Guardar**

### PASO 2: Copiar la URL de la Landing Page

Después de guardar, verás un campo llamado:
**"URL Landing Page"**

Ejemplo:
```
http://localhost:8069/product/landing/1
```

### PASO 3: Abrir la Landing Page

1. Copia esa URL
2. Ábrela en una **nueva pestaña** del navegador
3. Verás el formulario de registro con:
   - 👤 Nombre completo
   - 📱 Número de WhatsApp
   - 📧 Correo electrónico

---

## 🎯 DIFERENCIAS ENTRE LAS DOS LANDING PAGES

### Landing Page del Chatbot (la que estás viendo)
- **URL:** `http://localhost:8069/chatbot`
- **Propósito:** Chatear con Gemini AI
- **Contenido:** Robot, subir archivos, chat
- **NO tiene formulario de registro**

### Landing Page de Producto (la que necesitas)
- **URL:** `http://localhost:8069/product/landing/{id}`
- **Propósito:** Capturar leads para WhatsApp
- **Contenido:** Formulario de registro
- **SÍ tiene:** Nombre, WhatsApp, Email

---

## 📝 EJEMPLO VISUAL

### Lo que estás viendo ahora (INCORRECTO):
```
┌─────────────────────────────────┐
│  🤖 Gemini AI Chatbot          │
│                                 │
│  ⚡ IA Avanzada                │
│  💬 Chat Interactivo           │
│  ⚙️ Personalizable             │
│  📜 Historial                  │
│                                 │
│  📤 Subir Archivos Excel       │
│                                 │
│  [Botón flotante de chat]      │
└─────────────────────────────────┘
```

### Lo que deberías ver (CORRECTO):
```
┌─────────────────────────────────┐
│     MacBook Pro                 │
│  MacBook Pro en venta           │
│                                 │
│  📱 ¡Regístrate Ahora!         │
│                                 │
│  👤 Nombre completo             │
│  [___________________]          │
│                                 │
│  📱 Número de WhatsApp         │
│  [___________________]          │
│                                 │
│  📧 Correo electrónico         │
│  [___________________]          │
│                                 │
│  [Enviar información]           │
└─────────────────────────────────┘
```

---

## 🔍 VERIFICAR QUE FUNCIONA

### Prueba rápida:

1. Abre: `http://localhost:8069/product/landing/1`
2. Si ves el formulario de registro → ✅ Correcto
3. Si ves el chatbot → ❌ URL incorrecta

---

## 🆘 SI NO FUNCIONA

### Error: "Página no encontrada"

**Causa:** No existe una campaña con ese ID

**Solución:**
1. Ve a: Gemini Chatbot > Campañas WhatsApp
2. Crea una campaña nueva
3. Después de guardar, copia la URL que aparece
4. Usa esa URL

### Error: "No se puede acceder"

**Causa:** Odoo no está corriendo

**Solución:**
```bash
docker-compose up -d
```

---

## 📊 MENÚ DE NAVEGACIÓN EN ODOO

Para acceder a las campañas:

```
Odoo
└── Gemini Chatbot (menú principal)
    ├── Abrir Landing Page ← Esta es del chatbot (NO)
    ├── Chat Sessions
    ├── Leads Registrados
    ├── Campañas WhatsApp ← AQUÍ están las landing pages (SÍ)
    ├── Messages
    └── Subidas de Archivos
```

---

## ✅ RESUMEN

1. **NO uses** el menú "Abrir Landing Page" (es del chatbot)
2. **SÍ usa** la URL de "Campañas WhatsApp"
3. La URL correcta es: `/product/landing/{id}`
4. Cada campaña tiene su propia landing page

---

## 🎯 PRÓXIMOS PASOS

1. Ve a: **Gemini Chatbot > Campañas WhatsApp**
2. Abre o crea una campaña
3. Copia la **URL Landing Page**
4. Ábrela en el navegador
5. Verás el formulario de registro
6. Prueba registrándote
7. Ve a **Leads Registrados** para ver tu registro

---

**¡Ahora sí podrás ver el formulario de registro! 📱**
