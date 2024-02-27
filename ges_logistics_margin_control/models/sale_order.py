# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    

    below_margin = fields.Boolean(string="Below Min. Margin", default=False, compute_sudo=True, compute="_compute_below_margin")
    approved_below_margin = fields.Boolean(string="Below Margin Approved")
    approved_price_unit = fields.Float(string="Approved Price Unit")
    

    @api.onchange('pricelist_item_id','margin_percent')
    @api.depends('pricelist_item_id','margin_percent')
    def _compute_below_margin(self):
        for record in self:
            record.below_margin = False
            if record.pricelist_item_id and record.pricelist_item_id.compute_price == 'formula' and record.pricelist_item_id.base == 'standard_price' and record._get_pricelist_price() == 0:
                if (record.pricelist_item_id.price_discount * -1) >= (record.margin_percent * 100):
                    record.below_margin = True