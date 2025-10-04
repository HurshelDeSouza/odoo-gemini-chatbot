from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class ChatbotController(http.Controller):

    @http.route('/chatbot', type='http', auth='public', website=True)
    def chatbot_landing(self, **kwargs):
        """Chatbot landing page"""
        return request.render('gemini_chatbot.chatbot_landing_template')
    
    @http.route('/chatbot/register_lead', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def register_lead(self, **post):
        """Registra un lead desde la landing page del chatbot"""
        try:
            # Verificar si el teléfono ya existe
            existing_lead = request.env['gemini.product.lead'].sudo().search([
                ('phone', '=', post.get('phone'))
            ], limit=1)
            
            if existing_lead:
                return json.dumps({
                    'success': False,
                    'error': 'Este número de teléfono ya está registrado. Si ya te registraste antes, te contactaremos pronto.'
                })
            
            # Crear el lead
            lead = request.env['gemini.product.lead'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'campaign_id': False,  # No está asociado a ninguna campaña específica
            })
            
            return json.dumps({
                'success': True,
                'message': '¡Gracias! Tu información ha sido registrada correctamente.'
            })
        except Exception as e:
            error_msg = str(e)
            _logger.error(f"Error al registrar lead: {error_msg}")
            
            # Manejar error de duplicado de la base de datos
            if 'phone_unique' in error_msg or 'duplicate key' in error_msg.lower():
                return json.dumps({
                    'success': False,
                    'error': 'Este número de teléfono ya está registrado. Si ya te registraste antes, te contactaremos pronto.'
                })
            
            return json.dumps({
                'success': False,
                'error': 'Error al procesar tu solicitud. Por favor, intenta nuevamente.'
            })
    
    @http.route('/chatbot/send_message', type='json', auth='public', methods=['POST'])
    def send_message(self, message=None, session_id=None, **kwargs):
        """Send message to chatbot"""
        try:
            _logger.info(f"Received message: {message}, session_id: {session_id}, kwargs: {kwargs}")
            
            if not message:
                return {
                    'success': False,
                    'error': 'Message is required'
                }
            
            # Get or create session
            if not session_id:
                session = request.env['chat.session'].sudo().create({
                    'user_id': request.env.user.id if not request.env.user._is_public() else False,
                })
                session_id = session.id
            
            # Send message to Gemini
            result = request.env['chat.message'].sudo().send_message_to_gemini(session_id, message)
            
            if result['success']:
                return {
                    'success': True,
                    'session_id': session_id,
                    'bot_response': result['bot_response'],
                    'tokens_used': result['tokens_used'],
                    'response_time': result['response_time']
                }
            else:
                return {
                    'success': False,
                    'error': result['error'],
                    'session_id': session_id
                }
                
        except Exception as e:
            _logger.error(f"Error in chatbot controller: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/chatbot/get_history', type='json', auth='public', methods=['POST'])
    def get_chat_history(self, session_id=None, **kwargs):
        """Get chat history for a session"""
        try:
            if not session_id:
                return {
                    'success': False,
                    'error': 'Session ID is required'
                }
            
            messages = request.env['chat.message'].sudo().search([
                ('session_id', '=', session_id)
            ], order='create_date asc')
            
            history = []
            for msg in messages:
                history.append({
                    'id': msg.id,
                    'type': msg.message_type,
                    'content': msg.content,
                    'timestamp': msg.create_date.strftime('%H:%M'),
                    'tokens_used': msg.tokens_used
                })
            
            return {
                'success': True,
                'history': history
            }
            
        except Exception as e:
            _logger.error(f"Error getting chat history: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/chatbot/new_session', type='json', auth='public', methods=['POST'])
    def new_session(self):
        """Create a new chat session"""
        try:
            session = request.env['chat.session'].sudo().create({
                'user_id': request.env.user.id if not request.env.user._is_public() else False,
            })
            
            return {
                'success': True,
                'session_id': session.id
            }
            
        except Exception as e:
            _logger.error(f"Error creating new session: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }