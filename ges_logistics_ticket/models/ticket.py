# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from pytz import timezone

class Ticket(models.Model):
    _name = 'ticket'
    _description = "Tickets"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "action"
    
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')

    user_id = fields.Many2one('res.users', string='User', no_sort=True)
    requester_user_id = fields.Many2one('res.users', string='User', no_sort=True)

    state = fields.Selection([('open','Open'),('closed','Closed'),('cancel','Cancelled')], string="Status")

    opened_datetime = fields.Datetime(string="Opened On")
    closed_datetime = fields.Datetime(string="Closed On")
    open_duration = fields.Float(string="Open Duration (Hours)", compute="_compute_open_duration")
    
    tickt_action_selections = [
    ]
    action = fields.Selection(selection=tickt_action_selections, string="Action", no_sort=True)
    
    reference_document_selections = [
    ]
    reference_document = fields.Reference(selection=reference_document_selections, string="Ref Doc")
    

    note = fields.Text(string="Notes")

    @api.depends('opened_datetime','closed_datetime')
    def _compute_open_duration(self):
        for record in self:
            record.open_duration = 0
            if record.closed_datetime:
                record.open_duration = (record.closed_datetime - record.opened_datetime).total_seconds() / 60 / 60

    