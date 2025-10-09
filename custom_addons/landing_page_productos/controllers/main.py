# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class LandingPageController(http.Controller):
    
    @http.route('/landing/productos', type='http', auth='public', website=True)
    def landing_page(self, **kwargs):
        """Renderiza la landing page"""
        products = request.env['product.template'].sudo().search([('sale_ok', '=', True)], limit=10)
        return request.render('landing_page_productos.landing_template', {
            'products': products,
        })
    
    @http.route('/landing/submit', type='json', auth='public', methods=['POST'], csrf=False)
    def submit_lead(self, **post):
        """Recibe el formulario y crea un lead en el CRM"""
        try:
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            product_interest = post.get('product_interest')
            message = post.get('message', '')
            
            # Crear lead en CRM
            lead_vals = {
                'name': f'Lead - {name}',
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': f'Producto de interés: {product_interest}\n\nMensaje: {message}',
                'type': 'lead',
                'source_id': request.env.ref('utm.utm_source_website').id,
            }
            
            lead = request.env['crm.lead'].sudo().create(lead_vals)
            
            return {
                'success': True,
                'message': '¡Gracias! Nos pondremos en contacto contigo pronto.',
                'lead_id': lead.id
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al enviar el formulario: {str(e)}'
            }
