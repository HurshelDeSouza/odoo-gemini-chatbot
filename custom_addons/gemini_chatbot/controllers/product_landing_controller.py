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
            # Crear el lead
            lead = request.env['gemini.product.lead'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'campaign_id': campaign_id,
            })
            
            # Exportar a Drive
            lead.export_to_drive()
            
            return json.dumps({'success': True})
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)})