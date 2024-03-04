# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FleetShipment(models.Model):
    _inherit = 'fleet.vehicle'

    is_freight_shipment = fields.Boolean()
    partner_id = fields.Many2one('res.partner', string="Account")