# 📱 Landing Page + WhatsApp Integration

## ✅ IMPLEMENTACIÓN COMPLETADA

### 🎯 Funcionalidad

La landing page ahora captura:
- 👤 **Nombre completo**
- 📱 **Número de WhatsApp**
- 📧 **Correo electrónico**

Estos datos se guardan en la base de datos y se pueden usar para enviar mensajes de difusión por WhatsApp.

---

## 🚀 CÓMO FUNCIONA

### 1. Usuario visita la Landing Page

**URL:** `http://localhost:8069/product/landing/{campaign_id}`

La landing page muestra:
- Información del producto/campaña
- Formulario de registro atractivo
- Validación de datos en tiempo real

### 2. Usuario se registra

El usuario ingresa:
- Nombre: "Juan Pérez"
- WhatsApp: "5353065305" (con código de país, sin +)
- Email: "juan@email.com"

### 3. Datos se guardan automáticamente

Los datos se guardan en el modelo `gemini.product.lead`:
- Se asocian a la campaña correspondiente
- Se registra fecha y hora
- Quedan disponibles para envío de WhatsApp

---

## 📊 VER LEADS REGISTRADOS

### En Odoo:

1. Ve a: **Gemini Chatbot > Leads Registrados**
2. Verás todos los usuarios que se han registrado
3. Puedes ver: nombre, teléfono, email, campaña, fecha

---

## 📤 EXPORTAR LEADS PARA WHATSAPP

### Opción 1: Exportar a CSV

1. Ve a: **Gemini Chatbot > Leads Registrados**
2. Selecciona los leads que quieres exportar
3. Clic en: **Exportar a CSV**
4. Se descarga un archivo CSV con formato:
   ```csv
   nombre,whatsapp,email
   Juan Pérez,5353065305,juan@email.com
   María García,573001234567,maria@email.com
   ```

### Opción 2: Usar directamente en campaña

1. Exporta los leads a CSV
2. Ve a: **Gemini Chatbot > Campañas WhatsApp**
3. Crea nueva campaña
4. Sube el CSV exportado
5. Escribe tu mensaje
6. Envía mensajes masivos

---

## 🎨 CARACTERÍSTICAS DE LA LANDING PAGE

### Diseño Mejorado:
- ✅ Diseño moderno y atractivo
- ✅ Responsive (funciona en móviles)
- ✅ Colores llamativos (gradiente morado/azul)
- ✅ Iconos visuales (📱, 👤, 📧)
- ✅ Animaciones suaves

### Validación:
- ✅ Campos obligatorios
- ✅ Validación de email
- ✅ Solo números en teléfono
- ✅ Mensajes de error/éxito

### Experiencia de Usuario:
- ✅ Botón con estado de carga
- ✅ Mensajes de confirmación
- ✅ Formulario se limpia después de enviar
- ✅ Instrucciones claras

---

## 📝 EJEMPLO DE USO COMPLETO

### Paso 1: Crear Campaña

1. Ve a: **Gemini Chatbot > Campañas WhatsApp**
2. Crea campaña: "Venta MacBook Pro"
3. Producto: "MacBook Pro 2024"
4. Descripción: "MacBook Pro M3, 16GB RAM, 512GB SSD"
5. Guarda

### Paso 2: Compartir Landing Page

La URL de la landing page se genera automáticamente:
```
http://localhost:8069/product/landing/1
```

Comparte esta URL en:
- Redes sociales
- Email marketing
- Anuncios
- WhatsApp Status

### Paso 3: Usuarios se Registran

Los usuarios visitan la landing page y se registran con sus datos.

### Paso 4: Exportar Leads

1. Ve a: **Leads Registrados**
2. Selecciona todos los leads
3. Exporta a CSV

### Paso 5: Enviar Mensajes de WhatsApp

1. Ve a: **Campañas WhatsApp**
2. Crea nueva campaña de difusión
3. Sube el CSV exportado
4. Mensaje:
   ```
   ¡Hola {nombre}! 👋
   
   Gracias por tu interés en nuestro MacBook Pro.
   
   Tenemos una oferta especial para ti.
   
   Más info: {landing_url}
   ```
5. Envía mensajes

---

## 🔧 ARCHIVOS MODIFICADOS

### Vistas:
- ✅ `views/product_landing_views.xml` - Landing page mejorada
- ✅ `views/product_lead_views.xml` - Vista de leads (NUEVO)

### Controladores:
- ✅ `controllers/product_landing_controller.py` - Manejo de formulario

### Modelos:
- ✅ `models/whatsapp_campaign.py` - Modelo de leads + exportación

### Manifest:
- ✅ `__manifest__.py` - Agregada vista de leads

---

## 📱 FORMATO DE NÚMEROS

### Importante:
Los números deben tener código de país (sin +):

- ✅ Cuba: `5353065305`
- ✅ Colombia: `573001234567`
- ✅ México: `5215512345678`
- ❌ Incorrecto: `+53 5306 5305`
- ❌ Incorrecto: `53-5306-5305`

---

## 🎯 FLUJO COMPLETO

```
1. Usuario ve anuncio/link
   ↓
2. Visita Landing Page
   ↓
3. Se registra (nombre, WhatsApp, email)
   ↓
4. Datos se guardan en Odoo
   ↓
5. Admin exporta leads a CSV
   ↓
6. Admin crea campaña de WhatsApp
   ↓
7. Admin sube CSV y envía mensajes
   ↓
8. Usuarios reciben mensaje por WhatsApp
```

---

## 🆘 TROUBLESHOOTING

### Landing page no carga
- Verifica que Odoo esté corriendo
- Verifica la URL: `/product/landing/{campaign_id}`
- Verifica que la campaña exista

### Formulario no envía
- Verifica que todos los campos estén llenos
- Verifica formato de email
- Verifica que el número sea solo dígitos

### Leads no aparecen
- Ve a: Gemini Chatbot > Leads Registrados
- Verifica que el formulario se haya enviado correctamente
- Revisa logs de Odoo: `docker-compose logs -f web`

### Exportación no funciona
- Selecciona al menos un lead
- Clic en "Exportar a CSV"
- El archivo se descarga automáticamente

---

## 📊 ESTRUCTURA DE DATOS

### Modelo: gemini.product.lead

| Campo | Tipo | Descripción |
|-------|------|-------------|
| name | Char | Nombre completo |
| phone | Char | Número de WhatsApp |
| email | Char | Correo electrónico |
| campaign_id | Many2one | Campaña asociada |
| date | Datetime | Fecha de registro |

---

## ✅ VENTAJAS

1. **Captura automática** - Los datos se guardan sin intervención
2. **Base de datos centralizada** - Todo en Odoo
3. **Exportación fácil** - Un clic para exportar
4. **Integración WhatsApp** - Usa los datos para difusión
5. **Seguimiento** - Sabes qué campaña generó cada lead
6. **Escalable** - Maneja miles de registros

---

**¡Sistema completo de Landing Page + WhatsApp listo! 🎉**

Para probar:
1. Crea una campaña en Odoo
2. Visita la landing page
3. Regístrate con tus datos
4. Ve a "Leads Registrados"
5. Exporta y usa en WhatsApp
