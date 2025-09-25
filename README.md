# Odoo Gemini Chatbot

Este módulo integra un chatbot impulsado por Gemini AI en Odoo 18, permitiendo interacciones inteligentes con los usuarios.

## Características

- Integración con Gemini AI
- Gestión de sesiones de chat
- Interfaz de usuario amigable
- Panel de administración para configuración
- Historial de conversaciones
- Personalización de respuestas

## Requisitos

- Docker y Docker Compose
- Odoo 18.0
- PostgreSQL 16

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/HurshelDeSouza/odoo-gemini-chatbot.git
cd odoo-gemini-chatbot
```

2. Inicia los contenedores:
```bash
docker-compose up -d
```

3. Accede a Odoo:
- URL: http://localhost:8069
- Base de datos: odoo_test
- Usuario: admin
- Contraseña: admin

4. Instala el módulo:
- Ve a Aplicaciones
- Busca "Gemini Chatbot"
- Haz clic en Instalar

## Configuración

1. Ve a Configuración -> Gemini Chatbot
2. Configura tu API Key de Gemini
3. Personaliza las respuestas del chatbot según tus necesidades

## Estructura del Proyecto

```
custom_addons/
└── gemini_chatbot/
    ├── controllers/      # Controladores HTTP
    ├── models/          # Modelos de datos
    ├── security/        # Reglas de acceso
    ├── static/          # Archivos CSS/JS
    └── views/           # Vistas XML
```

## Soporte

Para reportar problemas o solicitar nuevas características, por favor abre un issue en este repositorio.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.