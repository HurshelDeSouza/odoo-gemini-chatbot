# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.model
    def get_or_create_company_by_country(self, country_code, country_name):
        """
        Obtiene o crea una compañía basada en el código de país
        """
        Company = self.env['res.company']
        Country = self.env['res.country']
        Currency = self.env['res.currency']
        
        # Buscar si ya existe una compañía para este país
        company = Company.search([
            ('name', '=', country_name)
        ], limit=1)
        
        if company:
            return company
        
        # Si no existe, crearla dinámicamente
        try:
            # Buscar el país
            country = Country.search([('code', '=', country_code.upper())], limit=1)
            if not country:
                _logger.warning('Country %s not found', country_code)
                return self.env.company
            
            # Obtener la moneda del país
            currency = country.currency_id or Currency.search([('name', '=', 'USD')], limit=1)
            
            # Crear la compañía
            company = Company.create({
                'name': country_name,
                'country_id': country.id,
                'currency_id': currency.id,
            })
            
            _logger.info('Created company: %s (ID: %s)', country_name, company.id)
            
            # Crear equipo de ventas para esta compañía
            self.env['crm.team'].create({
                'name': 'Website %s' % country_name,
                'company_id': company.id,
                'use_leads': True,
                'use_opportunities': True,
            })
            
            return company
            
        except Exception as e:
            _logger.error('Error creating company for %s: %s', country_name, e)
            return self.env.company
