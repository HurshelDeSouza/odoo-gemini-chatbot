from odoo import models, fields, api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ChatbotConfig(models.Model):
    _name = 'chatbot.config'
    _description = 'Chatbot Configuration'
    _rec_name = 'name'

    name = fields.Char('Configuration Name', required=True, default='Gemini Chatbot')
    api_key = fields.Char('Google API Key', required=True)
    model_name = fields.Selection([
        ('gemini-2.5-pro', 'Gemini 2.5 Pro - Razonamiento Avanzado'),
        ('gemini-2.5-flash', 'Gemini 2.5 Flash - Velocidad y Calidad'),
        ('gemini-2.5-flash-lite', 'Gemini 2.5 Flash Lite - Alto Volumen'),
    ], string='Gemini Model', default='gemini-2.5-flash', required=True)
    
    max_tokens = fields.Integer('Max Tokens', default=1000)
    temperature = fields.Float('Temperature', default=0.7, help='Controls randomness (0.0 to 1.0)')
    system_prompt = fields.Text('System Prompt', default='You are a helpful AI assistant.')
    
    active = fields.Boolean('Active', default=True)
    total_tokens_used = fields.Integer('Total Tokens Used', readonly=True)
    total_requests = fields.Integer('Total Requests', readonly=True)
    
    @api.model
    def get_active_config(self):
        """Get the active chatbot configuration"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            # Create default config if none exists
            config = self.create({
                'name': 'Default Gemini Config',
                'api_key': 'AIzaSyCJ9iSf09mzRYp1aBCf80GevebsO1nSvFE',
                'model_name': 'gemini-1.5-flash'
            })
        return config
    
    def test_connection(self):
        """Test the API connection"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/{self.model_name}:generateContent"
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                'contents': [{
                    'parts': [{'text': 'Hello, this is a test message.'}]
                }],
                'generationConfig': {
                    'maxOutputTokens': 10,
                    'temperature': 0.1
                }
            }
            
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success!',
                        'message': 'API connection successful',
                        'type': 'success',
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error!',
                        'message': f'API connection failed: {response.text}',
                        'type': 'danger',
                    }
                }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': f'Connection error: {str(e)}',
                    'type': 'danger',
                }
            }