# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StorageOrder(models.Model):
    _name = "logistics.storage.order"
    _description = "Storage Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)

    # linkage / creation fields
    source_sol_id = fields.Many2one('sale.order.line', string="Source SOL", store=False)
