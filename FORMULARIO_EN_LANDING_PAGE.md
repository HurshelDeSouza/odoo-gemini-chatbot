# ✅ FORMULARIO DE REGISTRO EN LANDING PAGE PRINCIPAL

## 🎯 LO QUE SE HIZO

Se agregó el formulario de registro directamente en la landing page principal del chatbot (`/chatbot`).

Ahora cuando los clientes vean un producto y estén interesados, pueden registrarse directamente en esa página.

---

## 📱 CÓMO SE VE AHORA

### URL: `http://localhost:8069/chatbot`

```
┌─────────────────────────────────────┐
│                                     │
│      ventas de quesos               │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  📱 ¡Regístrate Ahora!             │
│                                     │
│  Déjanos tus datos y te enviaremos │
│  más información por WhatsApp       │
│                                     │
│  👤 Nombre completo                │
│  [___________________________]      │
│                                     │
│  📱 Número de WhatsApp             │
│  [___________________________]      │
│  Ingresa tu número con código...    │
│                                     │
│  📧 Correo electrónico             │
│  [___________________________]      │
│                                     │
│  [✉️ Enviar información]           │
└─────────────────────────────────────┘
```

---

## 🚀 CARACTERÍSTICAS

### Formulario Completo:
- ✅ Nombre completo
- ✅ Número de WhatsApp (con validación)
- ✅ Correo electrónico
- ✅ Botón de envío

### Validaciones:
- ✅ Campos obligatorios
- ✅ Formato de email
- ✅ Solo números en WhatsApp
- ✅ Mensajes de error/éxito

### Experiencia de Usuario:
- ✅ Diseño atractivo (gradiente morado/azul)
- ✅ Responsive (funciona en móviles)
- ✅ Animaciones suaves
- ✅ Feedback visual
- ✅ Botón con estado de carga

---

## 📊 FLUJO COMPLETO

```
1. Cliente ve producto/servicio
   ↓
2. Visita: http://localhost:8069/chatbot
   ↓
3. Ve el título: "ventas de quesos"
   ↓
4. Llena el formulario de registro
   ↓
5. Hace clic en "Enviar información"
   ↓
6. Datos se guardan en Odoo
   ↓
7. Aparece mensaje de confirmación
   ↓
8. Admin puede ver el lead en "Leads Registrados"
   ↓
9. Admin exporta a CSV
   ↓
10. Admin envía mensaje por WhatsApp
```

---

## 🔧 ARCHIVOS MODIFICADOS/CREADOS

### Nuevos:
- ✅ `views/chatbot_landing_simple.xml` - Nueva vista con formulario
- ✅ `FORMULARIO_EN_LANDING_PAGE.md` - Esta documentación

### Modificados:
- ✅ `controllers/chatbot_controller.py` - Endpoint `/chatbot/register_lead`
- ✅ `__manifest__.py` - Vista agregada

---

## 📝 CÓMO PERSONALIZAR EL TÍTULO

Para cambiar "ventas de quesos" por otro texto:

1. Abre: `custom_addons/gemini_chatbot/views/chatbot_landing_simple.xml`
2. Busca la línea:
   ```xml
   <h1 class="product-title">ventas de quesos</h1>
   ```
3. Cambia el texto por el que quieras:
   ```xml
   <h1 class="product-title">MacBook Pro en Venta</h1>
   ```
4. Guarda y reinicia Odoo:
   ```bash
   docker-compose restart web
   ```

---

## 🎨 PERSONALIZACIÓN AVANZADA

### Cambiar colores:

En el archivo `chatbot_landing_simple.xml`, busca:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Cambia los colores por los que quieras:
- `#667eea` - Color inicial (azul)
- `#764ba2` - Color final (morado)

### Cambiar texto del botón:

Busca:
```xml
<button type="submit" class="btn-submit" id="submitBtn">
    <i class="fa fa-paper-plane"></i> Enviar información
</button>
```

Cambia "Enviar información" por lo que quieras.

---

## 📱 ACCESO

### URL Principal:
```
http://localhost:8069/chatbot
```

### Desde el menú de Odoo:
1. Gemini Chatbot
2. Abrir Landing Page

---

## 🔍 VER LEADS REGISTRADOS

### En Odoo:

1. Ve a: **Gemini Chatbot > Leads Registrados**
2. Verás todos los usuarios que se registraron
3. Campos mostrados:
   - Nombre
   - Teléfono (WhatsApp)
   - Email
   - Fecha de registro

### Exportar para WhatsApp:

1. Selecciona los leads
2. Clic en: **Exportar a CSV**
3. Usa el CSV en: **Campañas WhatsApp**

---

## ✅ VENTAJAS

1. **Una sola página** - Todo en un lugar
2. **Fácil de compartir** - Una sola URL
3. **Captura automática** - Los datos se guardan solos
4. **Listo para WhatsApp** - Exporta y envía mensajes
5. **Personalizable** - Cambia título y colores fácilmente

---

## 🆘 TROUBLESHOOTING

### Formulario no aparece

**Solución:**
1. Verifica que Odoo esté corriendo
2. Limpia caché del navegador (Ctrl+F5)
3. Verifica la URL: `http://localhost:8069/chatbot`

### Formulario no envía

**Solución:**
1. Verifica que todos los campos estén llenos
2. Verifica formato de email
3. Verifica que el número sea solo dígitos
4. Revisa logs: `docker-compose logs -f web`

### Leads no aparecen

**Solución:**
1. Ve a: Gemini Chatbot > Leads Registrados
2. Verifica que el formulario se haya enviado correctamente
3. Busca mensaje de confirmación verde

---

## 📊 EJEMPLO DE USO

### Caso: Venta de Quesos

1. **Personaliza el título:**
   - Cambia "ventas de quesos" por tu producto

2. **Comparte la URL:**
   - Redes sociales: "Visita http://localhost:8069/chatbot"
   - WhatsApp Status
   - Email marketing
   - Anuncios

3. **Clientes se registran:**
   - Ven el producto
   - Llenan el formulario
   - Reciben confirmación

4. **Tú exportas y envías:**
   - Exportas leads a CSV
   - Creas campaña de WhatsApp
   - Envías mensajes masivos

---

## 🎯 PRÓXIMOS PASOS

1. Personaliza el título del producto
2. Comparte la URL: `http://localhost:8069/chatbot`
3. Espera a que los clientes se registren
4. Exporta leads desde "Leads Registrados"
5. Envía mensajes por WhatsApp

---

**¡Formulario de registro listo en la landing page principal! 🎉**

Ahora los clientes pueden registrarse directamente cuando vean tu producto.
