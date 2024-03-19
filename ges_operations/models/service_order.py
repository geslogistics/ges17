# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Service Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')

    # record fields
    active = fields.Boolean(default=True, string='Active', tracking=True)
    color = fields.Integer('Color')
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())
    state_selection = [('new', 'Draft'), ('quotation', 'Quotation Sent'), ('booked', 'Booked'), ('inprogress', 'In Progress'), ('confirmed', 'Confirmed'), ('intransit', 'In Transit'), ('delivered', 'Delivered'), ('closed', 'Closed'), ('cancel', 'Cancelled')]
    state = fields.Selection(state_selection, string='Status', copy=False, tracking=True, default='new')

    # general order fields
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', string="Account")