# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools import email_normalize
import logging
from datetime import datetime
from markupsafe import Markup

_logger = logging.getLogger(__name__)

# Rate limiting simple (en memoria)
_rate_limit_cache = {}

class LandingPageController(http.Controller):
    
    def _get_company_by_phone(self, phone):
        """Detecta la compañía basándose en el código de país del teléfono"""
        if not phone:
            return request.env.company
        
        # Limpiar el teléfono de caracteres especiales
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Remover ceros iniciales (ej: 053065305 → 53065305)
        clean_phone = clean_phone.lstrip('0')
        
        # Mapeo de códigos telefónicos a países
        country_map = {
            '57': ('CO', 'Colombia'),
            '53': ('CU', 'Cuba'),
            '52': ('MX', 'México'),
            '1': ('US', 'USA'),
        }
        
        # Detectar país por código telefónico
        try:
            for code, (country_code, country_name) in country_map.items():
                if clean_phone.startswith(code):
                    # Obtener o crear compañía dinámicamente
                    company = request.env['crm.lead'].sudo().get_or_create_company_by_country(
                        country_code, country_name
                    )
                    return company
        except Exception as e:
            _logger.warning('Error detecting company by phone: %s', e)
        
        # Por defecto, usar la compañía actual
        return request.env.company
    
    def _get_team_by_company(self, company):
        """Obtiene el equipo de ventas de la compañía"""
        try:
            # Buscar equipo de ventas de la compañía
            team = request.env['crm.team'].sudo().search([
                ('company_id', '=', company.id),
                ('name', 'ilike', 'website')
            ], limit=1)
            
            if not team:
                # Si no hay equipo específico de website, buscar cualquier equipo
                team = request.env['crm.team'].sudo().search([
                    ('company_id', '=', company.id)
                ], limit=1)
            
            return team if team else False
        except Exception as e:
            _logger.warning('Error getting team by company: %s', e)
            return False
    
    @http.route('/landing/productos', type='http', auth='public', website=True)
    def landing_page(self, **kwargs):
        """Renderiza la landing page"""
        products = request.env['product.template'].sudo().search([('sale_ok', '=', True)], limit=10)
        return request.render('landing_page_productos.landing_template', {
            'products': products,
        })
    
    def _validate_email(self, email):
        """Valida el formato del email usando el validador de Odoo"""
        try:
            normalized = email_normalize(email)
            return bool(normalized)
        except Exception:
            return False
    
    def _check_rate_limit(self, ip_address, max_requests=5, time_window=300):
        """
        Rate limiting simple
        max_requests: máximo de solicitudes permitidas
        time_window: ventana de tiempo en segundos (300s = 5 minutos)
        """
        now = datetime.now()
        
        # Limpiar entradas antiguas
        expired_keys = [
            key for key, data in _rate_limit_cache.items()
            if (now - data['first_request']).total_seconds() > time_window
        ]
        for key in expired_keys:
            del _rate_limit_cache[key]
        
        # Verificar límite para esta IP
        if ip_address in _rate_limit_cache:
            data = _rate_limit_cache[ip_address]
            time_passed = (now - data['first_request']).total_seconds()
            
            if time_passed < time_window:
                if data['count'] >= max_requests:
                    return False, f'Demasiadas solicitudes. Intenta nuevamente en {int(time_window - time_passed)} segundos.'
                data['count'] += 1
            else:
                # Reiniciar contador
                _rate_limit_cache[ip_address] = {'count': 1, 'first_request': now}
        else:
            # Primera solicitud de esta IP
            _rate_limit_cache[ip_address] = {'count': 1, 'first_request': now}
        
        return True, None
    
    def _sanitize_input(self, text, max_length=500):
        """Sanitiza y limita la longitud del texto"""
        if not text:
            return ''
        # Limitar longitud
        text = text[:max_length]
        # Escapar HTML
        return Markup.escape(text)
    
    @http.route('/landing/submit', type='json', auth='public', methods=['POST'], csrf=False)
    def submit_lead(self, **post):
        """Recibe el formulario y crea un lead en el CRM"""
        try:
            # Rate limiting por IP
            ip_address = request.httprequest.remote_addr
            rate_ok, rate_message = self._check_rate_limit(ip_address)
            if not rate_ok:
                _logger.warning('Rate limit exceeded for IP: %s', ip_address)
                return {'success': False, 'message': rate_message}
            
            # Validar y sanitizar datos requeridos
            name = self._sanitize_input(post.get('name', '').strip(), 100)
            email = post.get('email', '').strip().lower()
            phone = post.get('phone', '').strip()
            product_interest = self._sanitize_input(post.get('product_interest', '').strip(), 200)
            message = self._sanitize_input(post.get('message', '').strip(), 1000)
            
            # Validación de campos requeridos
            if not name or not email or not phone:
                return {
                    'success': False,
                    'message': 'Por favor completa todos los campos requeridos.'
                }
            
            # Validación de email
            if not self._validate_email(email):
                return {
                    'success': False,
                    'message': 'Por favor ingresa un email válido.'
                }
            
            # Validación de teléfono (mínimo 7 dígitos)
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 7:
                return {
                    'success': False,
                    'message': 'Por favor ingresa un teléfono válido.'
                }
            
            # Detectar compañía por código de país del teléfono
            company = self._get_company_by_phone(phone)
            team = self._get_team_by_company(company)
            
            # Obtener source_id si existe
            source = request.env.ref('utm.utm_source_website', raise_if_not_found=False)
            
            # Obtener usuario técnico
            try:
                technical_user = request.env.ref('landing_page_productos.user_landing_page_technical', raise_if_not_found=False)
            except Exception:
                technical_user = None
            
            # Preparar valores del lead
            lead_vals = {
                'name': f'Lead - {name}',
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': f'Producto de interés: {product_interest}\n\nMensaje: {message}',
                'company_id': company.id,
                'team_id': team.id if team else False,
                'user_id': False,  # Sin asignar vendedor inicialmente
                'type': 'lead',  # Forzar tipo "lead" en lugar de "opportunity"
            }
            
            if source:
                lead_vals['source_id'] = source.id
            
            # Crear lead usando usuario técnico o sudo
            if technical_user:
                lead = request.env['crm.lead'].with_user(technical_user).with_context(tracking_disable=True).create(lead_vals)
                _logger.info('Lead created with technical user: %s (ID: %s)', lead.name, lead.id)
            else:
                lead = request.env['crm.lead'].with_context(tracking_disable=True).sudo().create(lead_vals)
                _logger.info('Lead created with sudo: %s (ID: %s)', lead.name, lead.id)
            
            return {
                'success': True,
                'message': '¡Gracias! Nos pondremos en contacto contigo pronto.',
                'lead_id': lead.id
            }
            
        except ValueError as e:
            _logger.warning('Validation error in landing form: %s', e)
            return {
                'success': False,
                'message': 'Datos inválidos. Por favor verifica la información.'
            }
        except Exception as e:
            _logger.error('Error creating lead from landing page: %s', e, exc_info=True)
            return {
                'success': False,
                'message': 'Ocurrió un error al enviar el formulario. Por favor intenta nuevamente.'
            }
