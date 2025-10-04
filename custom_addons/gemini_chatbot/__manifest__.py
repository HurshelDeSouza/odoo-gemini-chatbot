{
    'name': 'Gemini AI Chatbot',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'AI Chatbot powered by Google Gemini',
    'description': """
        Advanced AI Chatbot using Google Gemini API
        Features:
        - Multiple Gemini models support (Pro, Flash, etc.)
        - Chat history management
        - Token usage tracking
        - Modern chat interface
        - API key configuration
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'external_dependencies': {
        'python': ['requests'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/chatbot_config_views.xml',
        'views/chat_session_views.xml',
        'views/chat_message_views.xml',
        'views/file_upload_views.xml',
        'views/chatbot_landing_views.xml',
        'views/registration_landing.xml',
        'views/product_landing_views.xml',
        'views/whatsapp_campaign_views.xml',
        'views/product_lead_views.xml',
        'views/menu_views.xml',
        'data/chatbot_config_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gemini_chatbot/static/src/css/chatbot.css',
            'gemini_chatbot/static/src/js/chatbot.js',
        ],
        'web.assets_frontend': [
            'gemini_chatbot/static/src/css/chatbot_frontend.css',
            'gemini_chatbot/static/src/js/chatbot_frontend.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}