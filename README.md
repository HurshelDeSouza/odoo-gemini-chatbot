# Odoo Gemini Chatbot + WhatsApp Integration

Módulo completo de Odoo 18 con:
- 🤖 Chatbot impulsado por Gemini AI
- 📱 Integración de WhatsApp para envío masivo
- 🚀 API de WhatsApp con Node.js

## 🚀 Inicio Rápido

### 1. Iniciar Odoo
```bash
docker-compose up -d
```

### 2. Iniciar API de WhatsApp
```bash
cd whatsapp-api
Iniciar-API.bat
```
Escanea el QR con WhatsApp (solo primera vez)

### 3. Acceder a Odoo
- URL: http://localhost:8069
- Usuario: admin
- Contraseña: admin

## 📱 WhatsApp Integration

### Enviar mensajes
1. Ve a: **Gemini Chatbot > Campañas WhatsApp**
2. Crea campaña
3. Sube CSV con contactos
4. Envía mensajes

### Formato CSV
```csv
nombre,whatsapp,email
Cliente,5353065305,cliente@email.com
```

### Números soportados
- 🇨🇺 Cuba: 5353065305
- 🇨🇴 Colombia: 573001234567
- 🌍 Internacional: código + número

## 🤖 Gemini Chatbot

1. Ve a: **Configuración > Gemini Chatbot**
2. Configura tu API Key de Gemini
3. Personaliza respuestas

## 📂 Estructura

```
├── whatsapp-api/              # API de WhatsApp (Node.js)
│   ├── server.js              # Servidor principal
│   └── Iniciar-API.bat        # Script de inicio
│
└── custom_addons/gemini_chatbot/
    ├── controllers/           # Controladores HTTP
    ├── models/                # Modelos de datos
    ├── services/              # Servicios (WhatsApp)
    ├── security/              # Reglas de acceso
    ├── static/                # Archivos CSS/JS
    └── views/                 # Vistas XML
```

## 🔧 Troubleshooting

### Verificar API de WhatsApp
```bash
curl http://localhost:3000/status
```

### Ver logs de Odoo
```bash
docker-compose logs -f web
```

### Reiniciar todo
```bash
docker-compose restart
```

## 📚 Documentación

- `README_WHATSAPP.md` - Guía completa de WhatsApp
- `PROBLEMA_SOLUCIONADO.md` - Detalles técnicos
- `test-envio.ps1` - Script de prueba
- `verificar-todo.bat` - Verificación completa

## ✅ Características

- ✅ Chatbot con Gemini AI
- ✅ Envío masivo de WhatsApp
- ✅ Detección automática de código de país
- ✅ Soporte multi-país
- ✅ Interfaz integrada en Odoo
- ✅ Gestión de campañas
- ✅ Historial de conversaciones

## 🆘 Soporte

Para problemas o nuevas características, abre un issue en este repositorio.

## 📄 Licencia

MIT License