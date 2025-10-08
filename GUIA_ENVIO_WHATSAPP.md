# 📱 Guía para Enviar Mensajes de Difusión por WhatsApp

## ✅ Mejoras Implementadas

El sistema ahora lee correctamente el archivo CSV/Excel que subes en el campo "Archivo Excel de Contactos" con las siguientes mejoras:

### 🔧 Características Nuevas:

1. **Detección automática del nombre del archivo** - El sistema muestra el nombre del archivo subido
2. **Mejor manejo de codificaciones** - Soporta UTF-8, Latin1, CP1252, ISO-8859-1
3. **Detección inteligente de separadores** - Detecta automáticamente comas (,), punto y coma (;), tabulaciones o pipes (|)
4. **Logs detallados** - Información completa del procesamiento en los logs de Odoo
5. **Validación mejorada** - Mensajes de error más claros y específicos
6. **Normalización automática de números** - Agrega códigos de país automáticamente

### 📋 Formatos de Números Soportados:

#### 🇨🇺 Cuba:
- `53065305` → Se convierte a `5353065305`
- `5353065305` → Ya está correcto

#### 🇨🇴 Colombia:
- `3001234567` → Se convierte a `573001234567`
- `573001234567` → Ya está correcto

#### 🇲🇽 México:
- `5512345678` → Se convierte a `525512345678`

#### 🌍 Internacional:
- Cualquier número con 10+ dígitos se acepta tal cual

---

## 🚀 Cómo Usar el Sistema

### Paso 1: Vincular WhatsApp con el número +5353065305

1. Abre una terminal y ejecuta:
   ```cmd
   cd whatsapp-api
   node server.js
   ```

2. Aparecerá un código QR en la terminal

3. En el teléfono con el número **+53 53065305**:
   - Abre WhatsApp
   - Ve a **Configuración** → **Dispositivos vinculados**
   - Toca **"Vincular un dispositivo"**
   - Escanea el código QR

4. Espera el mensaje: **"✅ WhatsApp está listo!"**

5. **NO CIERRES** la terminal mientras uses el sistema

---

### Paso 2: Preparar el Archivo CSV

Crea un archivo CSV con este formato:

```csv
nombre,whatsapp,email
Juan Pérez,573001234567,juan@email.com
María García,5353065305,maria@email.com
Carlos López,3012345678,carlos@email.com
```

**Importante:**
- La primera línea debe ser el encabezado
- Debe tener una columna llamada: `whatsapp`, `telefono`, `celular`, `phone` o similar
- Los números pueden tener o no el código de país
- No uses espacios, guiones o paréntesis en los números
- Puedes usar coma (,) o punto y coma (;) como separador

**Archivo de ejemplo incluido:** `ejemplo_contactos.csv`

---

### Paso 3: Crear Campaña en Odoo

1. Abre tu navegador en: http://localhost:8069

2. Inicia sesión:
   - Usuario: `admin`
   - Contraseña: `admin`

3. Ve a: **Gemini Chatbot** → **Campañas WhatsApp**

4. Haz clic en **"Crear"**

5. Completa los campos:
   - **Nombre de Campaña**: Ej. "Promoción Octubre 2025"
   - **Nombre del Producto**: Ej. "MacBook Pro"
   - **Descripción del Producto**: Descripción detallada
   - **Archivo Excel de Contactos**: Sube tu archivo CSV
   - **Plantilla de Mensaje**: Escribe tu mensaje

   Ejemplo de mensaje:
   ```
   Hola! 👋
   
   Te presentamos {product_name}
   
   Más información aquí: {landing_url}
   ```

6. Haz clic en **"Guardar"**

7. Haz clic en **"Enviar Mensajes WhatsApp"**

---

### Paso 4: Verificar el Envío

El sistema te mostrará una notificación con:
- ✅ Mensajes enviados exitosamente
- ❌ Mensajes fallidos (si los hay)

**Ver logs detallados:**
```cmd
docker logs -f odoo18_web
```

Verás información como:
```
📄 Total de líneas en el archivo: 6
📱 Línea 2: 3 columnas
📞 Número original: '573001234567'
🔢 Número limpio: '573001234567'
🇨🇴 Colombia (completo): 573001234567
✅ Número agregado: 573001234567
```

---

## 🔍 Solución de Problemas

### ❌ "WhatsApp no está conectado"
**Solución:** Asegúrate de que la API esté corriendo (`node server.js`) y que hayas escaneado el QR

### ❌ "No se encontró columna de WhatsApp"
**Solución:** Verifica que tu CSV tenga una columna llamada `whatsapp`, `telefono`, `celular` o `phone`

### ❌ "No se encontraron números válidos"
**Solución:** 
- Verifica que los números no tengan espacios, guiones o paréntesis
- Asegúrate de que sean números de celular válidos
- Revisa que tengan al menos 8 dígitos

### ❌ "Error al decodificar el archivo"
**Solución:** Guarda tu archivo CSV con codificación UTF-8

---

## 📊 Ejemplo Completo

**Archivo: contactos.csv**
```csv
nombre,whatsapp,email
Cliente 1,5353065305,cliente1@email.com
Cliente 2,573001234567,cliente2@email.com
Cliente 3,53065305,cliente3@email.com
Cliente 4,3009876543,cliente4@email.com
```

**Mensaje:**
```
¡Hola! 👋

Tenemos una oferta especial en {product_name}

Descubre más aquí: {landing_url}

¡No te lo pierdas!
```

**Resultado:**
- Los mensajes se enviarán desde **+53 53065305**
- Cada contacto recibirá el mensaje personalizado
- Habrá un delay de 2 segundos entre cada mensaje

---

## 📝 Notas Importantes

1. **Límite de WhatsApp**: No envíes más de 50-100 mensajes por hora para evitar bloqueos
2. **Delay entre mensajes**: El sistema espera 2 segundos entre cada mensaje
3. **Sesión persistente**: Solo necesitas escanear el QR una vez
4. **Cambiar de número**: Si quieres usar otro número, elimina la carpeta `.wwebjs_auth` y vuelve a escanear

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs: `docker logs -f odoo18_web`
2. Verifica la API: `curl http://localhost:3000/status`
3. Asegúrate de que el formato del CSV sea correcto

¡Listo para enviar mensajes! 🚀
