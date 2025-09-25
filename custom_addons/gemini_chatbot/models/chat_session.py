from odoo import models, fields, api
from datetime import datetime

class ChatSession(models.Model):
    _name = 'chat.session'
    _description = 'Chat Session'
    _order = 'create_date desc'
    _rec_name = 'session_name'

    session_name = fields.Char('Session Name', compute='_compute_session_name', store=True)
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', 'Contact')
    
    message_ids = fields.One2many('chat.message', 'session_id', 'Messages')
    message_count = fields.Integer('Message Count', compute='_compute_message_count')
    
    tokens_used = fields.Integer('Tokens Used', compute='_compute_tokens_used', store=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], default='active')
    
    last_message_date = fields.Datetime('Last Message', compute='_compute_last_message_date', store=True)
    
    @api.depends('create_date', 'user_id')
    def _compute_session_name(self):
        for record in self:
            if record.create_date:
                date_str = record.create_date.strftime('%Y-%m-%d %H:%M')
                user_name = record.user_id.name if record.user_id else 'Guest'
                record.session_name = f"Chat - {user_name} - {date_str}"
            else:
                record.session_name = "New Chat Session"
    
    @api.depends('message_ids')
    def _compute_message_count(self):
        for record in self:
            record.message_count = len(record.message_ids)
    
    @api.depends('message_ids.tokens_used')
    def _compute_tokens_used(self):
        for record in self:
            record.tokens_used = sum(record.message_ids.mapped('tokens_used'))
    
    @api.depends('message_ids.create_date')
    def _compute_last_message_date(self):
        for record in self:
            if record.message_ids:
                record.last_message_date = max(record.message_ids.mapped('create_date'))
            else:
                record.last_message_date = record.create_date
    
    def archive_session(self):
        """Archive the chat session"""
        self.status = 'archived'
    
    def activate_session(self):
        """Activate the chat session"""
        self.status = 'active'