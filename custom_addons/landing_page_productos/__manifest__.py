# -*- coding: utf-8 -*-
{
    'name': 'Landing Page Productos',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Landing page personalizada para captura de leads con productos',
    'description': """
        Landing page con diseño personalizado que captura leads
        y los envía automáticamente al CRM con el producto de interés.
    """,
    'author': 'Tu Empresa',
    'website': 'https://www.tuempresa.com',
    'license': 'LGPL-3',
    'depends': ['website', 'crm', 'product', 'sales_team'],
    'data': [
        'views/crm_menu_views.xml',
        'views/landing_page_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'landing_page_productos/static/src/css/landing_page.css',
            'landing_page_productos/static/src/js/landing_page.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
