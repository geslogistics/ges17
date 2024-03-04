# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FreightVessel(models.Model):
    _name = 'freight.vessel'
    _description = 'Freight Vessel'
    
    active = fields.Boolean(default=True, string='Active')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    global_zone = fields.Char(string='Global Zone')
    country_id = fields.Many2one('res.country', 'Country')
    
    imo_number = fields.Char(string="IMO")
    flag_state = fields.Char(string="Flag state")
    port_of_registry = fields.Char(string="Port of Registry")
    capacity = fields.Char(string="Cargo Capacity")
    engine = fields.Char(string="Type")
    engine_power = fields.Char(string="Power")
    speed = fields.Char(string="Speed(Knots)")

    partner_id = fields.Many2one('res.partner', string='Carrier Account')