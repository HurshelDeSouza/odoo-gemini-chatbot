# 📱 WhatsApp Integration - Odoo 18

Integración completa de WhatsApp con Odoo 18 usando whatsapp-web.js

## 🚀 Inicio Rápido

### 1. Iniciar API de WhatsApp
```bash
cd whatsapp-api
Iniciar-API.bat
```
- Escanea el código QR con WhatsApp (solo primera vez)
- Espera: "✅ WhatsApp está listo!"

### 2. Verificar API
```
http://localhost:3000/status
```
Debe mostrar: `{"status":"ready"}`

### 3. Usar en Odoo
1. Abre: http://localhost:8069
2. Ve a: **Gemini Chatbot > Campañas WhatsApp**
3. Crea campaña, sube CSV, envía mensajes

## 📄 Formato del CSV

```csv
nombre,whatsapp,email
Cliente,5353065305,cliente@email.com
```

## 🌍 Números Soportados

- 🇨🇺 **Cuba:** 5353065305 o 53065305
- 🇨🇴 **Colombia:** 573001234567 o 3001234567
- 🌍 **Internacional:** Código de país + número

## 🔧 Troubleshooting

### API no conecta
```bash
# Verificar estado
curl http://localhost:3000/status

# Ver logs de Odoo
docker-compose logs -f web
```

### Reiniciar todo
```bash
docker-compose restart
cd whatsapp-api
npm run api
```

## 📊 Estructura

```
whatsapp-api/          # API de Node.js
├── server.js          # Servidor principal
├── package.json       # Dependencias
└── Iniciar-API.bat    # Script de inicio

custom_addons/gemini_chatbot/
├── services/
│   └── whatsapp_service.py    # Servicio de integración
└── models/
    └── whatsapp_campaign.py   # Modelo de campañas
```

## ✅ Características

- ✅ Envío individual y masivo
- ✅ Detección automática de código de país
- ✅ Soporte multi-país (Cuba, Colombia, etc.)
- ✅ Interfaz integrada en Odoo
- ✅ Logs detallados
- ✅ Manejo de errores

## 🧪 Prueba Rápida

```bash
# Prueba directa con PowerShell
powershell -ExecutionPolicy Bypass -File test-envio.ps1

# O verificar todo
verificar-todo.bat
```

## 📝 Archivos Importantes

- `contacto_macbook.csv` - Ejemplo de CSV
- `test-envio.ps1` - Script de prueba
- `verificar-todo.bat` - Verificación completa
- `PROBLEMA_SOLUCIONADO.md` - Detalles técnicos

---

**¡Sistema listo para enviar mensajes de WhatsApp! 🎉**
