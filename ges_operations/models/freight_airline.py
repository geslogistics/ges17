# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FreightAirline(models.Model):
    _name = 'freight.airline'
    _description = 'Freight Airline'

    active = fields.Boolean(default=True, string='Active')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    icao = fields.Char(string='ICAO')
    country_id = fields.Many2one('res.country', 'Country')
    
    aircraft_type = fields.Char(string="Aircraft Type")
    capacity = fields.Char(string="Cargo Capacity")
    partner_id = fields.Many2one('res.partner', string='Airline Account')