# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ShipmentItem(models.Model):
    _name = 'shipment.order.package.item'
    _description = 'Shipment Order Package Item'

    name = fields.Char(string='Description')
    package_line_id = fields.Many2one('shipment.order.package', 'Package')
    package = fields.Many2one('freight.package', 'Item')
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer')]), string="Operation")
    qty = fields.Float('Qty', default=1.0)
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('package')
    def onchange_package_id(self):
        for line in self:
            if line.package_line_id.shipment_order_id.transport == 'air':
                return {'domain': {'package': [('air', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_order_id.transport == 'ocean':
                return {'domain': {'package': [('ocean', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_order_id.transport == 'road':
                return {'domain': {'package': [('road', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_order_id.transport == 'rail':
                return {'domain': {'package': [('rail', '=', True), ('is_item', '=', True), ('active', '=', True)]}}

    @api.onchange('package')
    def _onchange_item_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.metric_volume
                rec.gross_weight = rec.package.metric_gross_weight
                rec.height = rec.package.metric_height
                rec.length = rec.package.metric_length
                rec.width = rec.package.metric_width
                rec.name = rec.package.desc