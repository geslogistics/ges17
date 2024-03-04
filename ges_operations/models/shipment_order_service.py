# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class ShipmentOrderService(models.Model):
    _name = "shipment.order.service"
    _rec_name = 'product_id'
    _description = "Shipment Order Service"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    shipment_order_id = fields.Many2one('shipment.order', string="Shipment Order")
    service_at = fields.Selection(([('pre-carriage', 'Pre-Carriage'), ('on-carriage', 'On-Carriage')]), string='Service At', default="pre-carriage")

    company_id = fields.Many2one(string="Company", related="shipment_order_id.company_id")

    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string="Color", related="shipment_order_id.color")
    sequence = fields.Integer(string="Sequence")
    
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())

    # Services


    partner_type = fields.Selection([('shipper', 'Shipper'), ('consignee', 'Consignee'), ('agent', 'Agent'), ('vendor','Vendor')], default="shipper", string="Service To")
    
    

    sol_id = fields.Many2many('sale.order.line', string="Charge")
    
    so_id = fields.Many2one('sale.order', related="sol_id.order_id")
    partner_id = fields.Many2one('res.partner', string="Account", related="so_id.partner_id")
    currency_id = fields.Many2one(string="Currency", related="so_id.currency_id")

    product_id = fields.Many2one('product.product', string="Service", related="sol_id.product_id")
    product_uom = fields.Many2one('uom.uom', string="Unit", related="sol_id.product_uom")
    product_uom_qty = fields.Float(string="Quantity", related="sol_id.product_uom_qty")
    name = fields.Text(string='Description', related="sol_id.name")

    price_unit = fields.Float(string="Unit Price", related="sol_id.price_unit")
    purchase_price = fields.Float(string="Cost", related="sol_id.purchase_price")
    tax_id = fields.Many2many('account.tax', string="Taxes", related="sol_id.tax_id")
    price_subtotal = fields.Monetary(string="Tax Excl.", related="sol_id.price_subtotal")
    price_total = fields.Monetary(string="Tax Incl.", related="sol_id.price_total")

    margin = fields.Float(string="Margin", related="sol_id.margin")
    margin_percent = fields.Float(string="Margin (%)", related="sol_id.margin_percent")




