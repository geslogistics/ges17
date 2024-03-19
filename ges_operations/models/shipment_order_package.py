# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re

class ShipmentOrderPackage(models.Model):
    _name = 'shipment.order.package'
    _description = 'Shipment Order Package'
    _rec_name = 'package'

    name = fields.Char(string='Container Number', required=True)
    package_type = fields.Selection([('item', 'Box / Cargo'), ('container', 'Container / Box')], string="Package Type")
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('road', 'Road'),('rail','Rail')]), string='Transport')
    shipment_order_id = fields.Many2one('shipment.order', 'Shipment Order')
    company_id = fields.Many2one('res.company', string='Company', related="shipment_order_id.company_id")
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    package = fields.Many2one('freight.package', string='Size / Package', required=True)
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer'), ('flat_rock', 'Flat Rock'), ('open_top', 'Open Top'),
          ('other', 'Other')]), string="Type")
    qty = fields.Float('Qty', required=True, default=1.0)
    harmonize = fields.Char('Harmonize')
    temperature = fields.Char('Temperature')
    humidity = fields.Char(string="Humidity")
    ventilation = fields.Char(string="Ventilation")
    vgm = fields.Char('VGM', help='Verified gross mass')
    carrier_seal = fields.Char('Carrier Seal')
    seal_number = fields.Char('Seal Number')
    reference = fields.Char('Reference')
    dangerous_goods = fields.Boolean('Dangerous Goods')
    class_number = fields.Char('Class Number')
    un_number = fields.Char('UN Number')
    Package_group = fields.Char('Packaging Group:')
    imdg_code = fields.Char('IMDG Code', help='International Maritime Dangerous Goods Code')
    flash_point = fields.Char('Flash Point')
    material_description = fields.Text('Material Description')
    freight_item_lines = fields.One2many('shipment.order.package.item', 'package_line_id')
    route_id = fields.Many2one('shipment.order.route', 'Route')
    container_type = fields.Selection(
        [('GP', 'GP (General Purpose)'), ('HC', 'HC (High Cube)'),
         ('RF', 'RF (Reefer)'), ('FR', 'FR (Flat Rack)'),
         ('OT', 'OT (Open Top)'), ('GOH', 'GOH (Garment of Hanger)')], string="Type", default="GP")
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    net_weight = fields.Float(string="Net Weight (KG)")
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('name')
    def container_no_check_onchange(self):
        for rec in self:
            if rec.name:
                if len(rec.name) > 11:
                    raise ValidationError(
                        f"The container number exceeds the maximum length (11 characters): {rec.name}"
                    )
                if not re.match('^[A-Z]{4}[0-9]{7,}$', rec.name.upper()):
                    raise ValidationError(
                        f"You have Entered a Wrong Container Number or Format: {rec.name.upper()}\n"
                        "Format is ABCD1234567\n"
                        "First Four Characters Must be Alphabet and Last Seven Characters Must be Numeric"
                    )
                rec.name = rec.name.upper()

    @api.onchange('package')
    def _onchange_package_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.metric_volume
                rec.gross_weight = rec.package.metric_gross_weight
                rec.height = rec.package.metric_height
                rec.length = rec.package.metric_length
                rec.width = rec.package.metric_width

    @api.onchange('package', 'package_type')
    def onchange_package_id(self):
        for line in self:
            if line.package_type == "item":
                if line.shipment_order_id.transport == 'air':
                    return {'domain': {'package': [('air', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'ocean':
                    return {'domain': {'package': [('ocean', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'road':
                    return {'domain': {'package': [('road', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'rail':
                    return {'domain': {'package': [('rail', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            elif line.package_type == "container":
                if line.shipment_order_id.transport == 'air':
                    return {
                        'domain': {'package': [('air', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'ocean':
                    return {
                        'domain': {'package': [('ocean', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'road':
                    return {
                        'domain': {'package': [('road', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_order_id.transport == 'rail':
                    return {
                        'domain': {'package': [('rail', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
