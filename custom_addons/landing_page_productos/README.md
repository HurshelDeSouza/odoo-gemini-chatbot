# Landing Page Productos - Módulo Odoo 18

Módulo personalizado para crear una landing page de productos con captura de leads integrada al CRM.

## Características

- ✅ Diseño personalizado similar a landing pages de productos
- ✅ Formulario de captura de leads
- ✅ Integración automática con CRM de Odoo
- ✅ Selector de productos de interés
- ✅ Diseño responsive (móvil y desktop)
- ✅ Envío de datos vía AJAX
- ✅ Validación de formularios

## Instalación

1. Copia este módulo a la carpeta `custom_addons/`
2. Reinicia el servidor de Odoo
3. Ve a Aplicaciones → Actualizar lista de aplicaciones
4. Busca "Landing Page Productos"
5. Haz click en "Instalar"

## Configuración

### 1. Agregar imagen del producto

Coloca la imagen de tu producto en:
```
custom_addons/landing_page_productos/static/src/img/producto-placeholder.jpg
```

### 2. Personalizar textos

Edita el archivo `views/landing_page_template.xml` para cambiar:
- Título del producto
- Precios
- Textos de la oferta
- Garantía

### 3. Personalizar colores

Edita el archivo `static/src/css/landing_page.css` para ajustar:
- Colores de la barra superior
- Colores de botones
- Estilos generales

## Uso

Una vez instalado, la landing page estará disponible en:
```
http://localhost:8069/landing/productos
```

### Captura de Leads

Cuando un usuario completa el formulario:
1. Los datos se envían automáticamente al CRM
2. Se crea un nuevo Lead con:
   - Nombre del contacto
   - Email
   - Teléfono
   - Producto de interés (en la descripción)
   - Fuente: Website

### Exportar Leads a CSV

1. Ve a CRM → Leads
2. Filtra por los leads que necesites
3. Selecciona los registros
4. Click en Acción → Exportar
5. Selecciona los campos a exportar
6. Descarga el CSV

## Estructura del Módulo

```
landing_page_productos/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py              # Controlador de rutas y lógica
├── views/
│   ├── landing_page_template.xml  # Template HTML
│   └── assets.xml           # Carga de CSS y JS
├── static/
│   └── src/
│       ├── css/
│       │   └── landing_page.css   # Estilos personalizados
│       ├── js/
│       │   └── landing_page.js    # JavaScript del formulario
│       └── img/
│           └── .gitkeep     # Carpeta para imágenes
└── README.md
```

## Personalización Avanzada

### Agregar más campos al formulario

1. Edita `views/landing_page_template.xml` y agrega el campo HTML
2. Edita `static/src/js/landing_page.js` para capturar el valor
3. Edita `controllers/main.py` para procesar el nuevo campo

### Cambiar el equipo de ventas destino

En `controllers/main.py`, agrega al diccionario `lead_vals`:
```python
'team_id': request.env.ref('crm.team_sales_department').id,
```

## Soporte

Para dudas o problemas, contacta al desarrollador.
