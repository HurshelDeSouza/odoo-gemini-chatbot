# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class LandingPageController(http.Controller):
    
    def _get_company_by_phone(self, phone):
        """Detecta la compañía basándose en el código de país del teléfono"""
        if not phone:
            return request.env.company
        
        # Limpiar el teléfono de caracteres especiales
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Detectar país por código telefónico usando XML IDs
        try:
            if clean_phone.startswith('57'):  # Colombia
                company = request.env.ref('landing_page_productos.company_colombia', raise_if_not_found=False)
                return company or request.env.company
            elif clean_phone.startswith('52'):  # México
                company = request.env.ref('landing_page_productos.company_mexico', raise_if_not_found=False)
                return company or request.env.company
            elif clean_phone.startswith('1'):  # USA/Canadá
                company = request.env.ref('landing_page_productos.company_usa', raise_if_not_found=False)
                return company or request.env.company
        except Exception as e:
            _logger.warning('Error detecting company by phone: %s', e)
        
        # Por defecto, usar la compañía actual
        return request.env.company
    
    def _get_team_by_company(self, company):
        """Obtiene el equipo de ventas de la compañía"""
        # Mapeo de compañías a equipos usando XML IDs
        company_team_map = {
            'landing_page_productos.company_colombia': 'landing_page_productos.sales_team_colombia_website',
            'landing_page_productos.company_mexico': 'landing_page_productos.sales_team_mexico_website',
            'landing_page_productos.company_usa': 'landing_page_productos.sales_team_usa_website',
        }
        
        try:
            # Buscar el XML ID de la compañía
            for company_xmlid, team_xmlid in company_team_map.items():
                company_ref = request.env.ref(company_xmlid, raise_if_not_found=False)
                if company_ref and company_ref.id == company.id:
                    team = request.env.ref(team_xmlid, raise_if_not_found=False)
                    return team if team else False
        except Exception as e:
            _logger.warning('Error getting team by company: %s', e)
        
        # Fallback: buscar cualquier equipo de la compañía
        team = request.env['crm.team'].sudo().search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        return team if team else False
    
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
            # Validar datos requeridos
            name = post.get('name', '').strip()
            email = post.get('email', '').strip()
            phone = post.get('phone', '').strip()
            product_interest = post.get('product_interest', '').strip()
            message = post.get('message', '').strip()
            
            if not name or not email or not phone:
                return {
                    'success': False,
                    'message': 'Por favor completa todos los campos requeridos.'
                }
            
            # Detectar compañía por código de país del teléfono
            company = self._get_company_by_phone(phone)
            team = self._get_team_by_company(company)
            
            # Obtener source_id si existe
            source = request.env.ref('utm.utm_source_website', raise_if_not_found=False)
            
            # Crear lead en CRM
            lead_vals = {
                'name': f'Lead - {name}',
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': f'Producto de interés: {product_interest}\n\nMensaje: {message}',
                'company_id': company.id,
                'team_id': team.id if team else False,
                'user_id': False,  # Sin asignar vendedor inicialmente
            }
            
            if source:
                lead_vals['source_id'] = source.id
            
            lead = request.env['crm.lead'].with_context(tracking_disable=True).sudo().create(lead_vals)
            
            _logger.info('Lead created successfully: %s (ID: %s)', lead.name, lead.id)
            
            return {
                'success': True,
                'message': '¡Gracias! Nos pondremos en contacto contigo pronto.',
                'lead_id': lead.id
            }
            
        except Exception as e:
            _logger.error('Error creating lead from landing page: %s', e, exc_info=True)
            return {
                'success': False,
                'message': 'Ocurrió un error al enviar el formulario. Por favor intenta nuevamente.'
            }
