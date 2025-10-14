# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class LandingPageController(http.Controller):
    
    def _get_company_by_phone(self, phone):
        """Detecta la compañía basándose en el código de país del teléfono"""
        if not phone:
            return request.env.company.id
        
        # Limpiar el teléfono de caracteres especiales
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Detectar país por código telefónico
        if clean_phone.startswith('57'):  # Colombia
            company = request.env['res.company'].sudo().search([('name', '=', 'Colombia')], limit=1)
            return company.id if company else request.env.company.id
        elif clean_phone.startswith('52'):  # México
            company = request.env['res.company'].sudo().search([('name', '=', 'México')], limit=1)
            return company.id if company else request.env.company.id
        elif clean_phone.startswith('1'):  # USA/Canadá
            company = request.env['res.company'].sudo().search([('name', '=', 'USA')], limit=1)
            return company.id if company else request.env.company.id
        
        # Por defecto, usar la compañía actual
        return request.env.company.id
    
    def _get_team_by_company(self, company_id):
        """Obtiene el equipo de ventas de la compañía"""
        team = request.env['crm.team'].sudo().search([
            ('company_id', '=', company_id),
            ('name', 'ilike', 'website')
        ], limit=1)
        
        if not team:
            # Si no hay equipo específico, buscar cualquier equipo de la compañía
            team = request.env['crm.team'].sudo().search([
                ('company_id', '=', company_id)
            ], limit=1)
        
        return team.id if team else False
    
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
            
            # Detectar compañía por código de país del teléfono
            company_id = self._get_company_by_phone(phone)
            
            # Obtener source_id si existe
            try:
                source_id = request.env.ref('utm.utm_source_website').id
            except:
                source_id = False
            
            # Crear lead en CRM
            lead_vals = {
                'name': f'Lead - {name}',
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': f'Producto de interés: {product_interest}\n\nMensaje: {message}',
                'type': 'lead',
                'company_id': company_id,
                'team_id': self._get_team_by_company(company_id),
                'user_id': False,  # Sin asignar vendedor inicialmente
            }
            
            if source_id:
                lead_vals['source_id'] = source_id
            
            lead = request.env['crm.lead'].with_context(tracking_disable=True).sudo().create(lead_vals)
            
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
