# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.fields import Command
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = ['product.template']

    # adjust fields
    request_costing_required = fields.Boolean("Require Costing Request")


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    # adjust fields
    request_costing_id = fields.Many2one('request.costing', string="Costing Request")
    request_costing_required = fields.Boolean(string="Costing Request Required", related="product_template_id.request_costing_required")

    """
    def action_create_prt(self):
        result = {
            "name": "Costing Request",
            "type": "ir.actions.act_window",
            "res_model": "request.costing",
            "view_mode": "form",
            "context": {"default_so_line_id": self.id},
        }
        return result
    """

    def action_request_request_costing_wizard(self):
        result = {
            "name": "Request Costing Request Items",
            "type": "ir.actions.act_window",
            "res_model": "cmo.request.wizard",
            "view_mode": "form",
            "target":"new",
            "context": {
                "default_wizard_type": "new",
                "default_so_line_id": self.id,
                },
        }
        return result
    """
    @api.onchange('product_id', 'company_id', 'currency_id', 'product_uom', 'request_costing_id', 'request_costing_id.total_costing')
    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom', 'request_costing_id', 'request_costing_id.total_costing')
    def _compute_purchase_price(self):
        for line in self:
            if line.request_costing_id:
                line.purchase_price = line._convert_to_sol_currency(line.request_costing_id.total_costing if line.request_costing_id.total_costing else 0, line.product_id.cost_currency_id)
            else:
                if not line.product_id:
                    line.purchase_price = 0.0
                    continue
                line = line.with_company(line.company_id)
                # Convert the cost to the line UoM
                product_cost = line.product_id.uom_id._compute_price(line.product_id.standard_price,line.product_uom,)
                line.purchase_price = line._convert_to_sol_currency(product_cost, line.product_id.cost_currency_id)
    """


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    # add fields

    request_costing_id = fields.Many2one('request.costing', string="Costing Request")



