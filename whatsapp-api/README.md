# WhatsApp API

API de WhatsApp usando whatsapp-web.js para Odoo 18.

## 🚀 Inicio Rápido

```bash
Iniciar-API.bat
```

1. Escanea el QR con WhatsApp (solo primera vez)
2. Espera: "✅ WhatsApp está listo!"
3. NO cierres la ventana

## 🔍 Verificar

```
http://localhost:3000/status
```

## 📡 Endpoints

### GET /status
Estado de la conexión

### POST /send-message
Envío individual
```json
{
  "phone": "5353065305",
  "message": "Hola!"
}
```

### POST /send-bulk
Envío masivo
```json
{
  "phones": ["5353065305", "573001234567"],
  "message": "Hola a todos!"
}
```

## ⚠️ Importante

- La API debe estar siempre corriendo
- QR solo se escanea una vez
- Delay de 2 segundos entre mensajes masivos
