from odoo import http
from odoo.http import request
import json

class ProductLandingController(http.Controller):
    
    @http.route('/product/landing/<int:campaign_id>', type='http', auth='public', website=True)
    def product_landing(self, campaign_id, **kw):
        """Renderiza la landing page del producto"""
        campaign = request.env['gemini.whatsapp.campaign'].sudo().browse(campaign_id)
        return request.render('gemini_chatbot.product_landing_template', {
            'campaign': campaign
        })

    @http.route('/submit/lead/<int:campaign_id>', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def submit_lead(self, campaign_id, **post):
        """Procesa el envío del formulario de lead"""
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
                'campaign_id': campaign_id,
            })
            
            return json.dumps({
                'success': True,
                'message': '¡Gracias! Tu información ha sido registrada correctamente.'
            })
        except Exception as e:
            error_msg = str(e)
            
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