from odoo import models, fields, api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ChatMessage(models.Model):
    _name = 'chat.message'
    _description = 'Chat Message'
    _order = 'create_date asc'

    session_id = fields.Many2one('chat.session', 'Session', required=True, ondelete='cascade')
    message_type = fields.Selection([
        ('user', 'User'),
        ('bot', 'Bot'),
    ], required=True)
    
    content = fields.Text('Message Content', required=True)
    tokens_used = fields.Integer('Tokens Used', default=0)
    
    model_used = fields.Char('Model Used')
    response_time = fields.Float('Response Time (seconds)')
    
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    
    @api.model
    def send_message_to_gemini(self, session_id, user_message):
        """Send message to Gemini API and create response"""
        try:
            # Get session and config
            session = self.env['chat.session'].browse(session_id)
            config = self.env['chatbot.config'].get_active_config()
            
            if not config.api_key:
                raise ValueError("API Key not configured")
            
            # Create user message
            user_msg = self.create({
                'session_id': session_id,
                'message_type': 'user',
                'content': user_message,
                'user_id': self.env.user.id
            })
            
            # Get conversation history
            history = self._get_conversation_history(session_id)
            
            # Prepare API request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model_name}:generateContent"
            
            contents = []
            
            # Add system prompt if it's the first message
            if len(history) == 1:  # Only user message exists
                contents.append({
                    'parts': [{'text': config.system_prompt}],
                    'role': 'user'
                })
                contents.append({
                    'parts': [{'text': 'Understood. I will act as your helpful assistant.'}],
                    'role': 'model'
                })
            
            # Add conversation history
            for msg in history[:-1]:  # Exclude the current message
                role = 'user' if msg.message_type == 'user' else 'model'
                contents.append({
                    'parts': [{'text': msg.content}],
                    'role': role
                })
            
            # Add current user message
            contents.append({
                'parts': [{'text': user_message}],
                'role': 'user'
            })
            
            data = {
                'contents': contents,
                'generationConfig': {
                    'maxOutputTokens': config.max_tokens,
                    'temperature': config.temperature,
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            import time
            start_time = time.time()
            
            # Make API request
            response = requests.post(
                f"{url}?key={config.api_key}",
                headers=headers,
                json=data,
                timeout=60
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                response_data = response.json()
                
                if 'candidates' in response_data and response_data['candidates']:
                    bot_response = response_data['candidates'][0]['content']['parts'][0]['text']
                    
                    # Calculate tokens (approximate)
                    tokens_used = self._estimate_tokens(user_message + bot_response)
                    
                    # Create bot message
                    bot_msg = self.create({
                        'session_id': session_id,
                        'message_type': 'bot',
                        'content': bot_response,
                        'tokens_used': tokens_used,
                        'model_used': config.model_name,
                        'response_time': response_time,
                        'user_id': self.env.user.id
                    })
                    
                    # Update user message tokens
                    user_msg.tokens_used = tokens_used // 2  # Approximate split
                    
                    # Update config stats
                    config.total_tokens_used += tokens_used
                    config.total_requests += 1
                    
                    return {
                        'success': True,
                        'user_message_id': user_msg.id,
                        'bot_message_id': bot_msg.id,
                        'bot_response': bot_response,
                        'tokens_used': tokens_used,
                        'response_time': response_time
                    }
                else:
                    raise ValueError("No response from Gemini API")
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                _logger.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            _logger.error(f"Error sending message to Gemini: {str(e)}")
            # Create error message
            error_msg = self.create({
                'session_id': session_id,
                'message_type': 'bot',
                'content': f"Sorry, I encountered an error: {str(e)}",
                'user_id': self.env.user.id
            })
            
            return {
                'success': False,
                'error': str(e),
                'user_message_id': user_msg.id if 'user_msg' in locals() else None,
                'bot_message_id': error_msg.id
            }
    
    def _get_conversation_history(self, session_id):
        """Get conversation history for context"""
        return self.search([
            ('session_id', '=', session_id)
        ], order='create_date asc')
    
    def _estimate_tokens(self, text):
        """Estimate token count (rough approximation)"""
        # Rough estimation: 1 token ≈ 4 characters for English text
        return max(1, len(text) // 4)