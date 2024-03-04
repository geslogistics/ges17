# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FreightRailway(models.Model):
    _name = 'freight.railway'
    _description = 'Freight Railway'

    active = fields.Boolean(default=True, string='Active')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    country_id = fields.Many2one('res.country', 'Country')
    
    railway_type = fields.Char(string="Railway Type")
    capacity = fields.Char(string="Cargo Capacity")
    partner_id = fields.Many2one('res.partner', string='Railway Account')