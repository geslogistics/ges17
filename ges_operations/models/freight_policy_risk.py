# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class FreightPolicyRisk(models.Model):
    _name = 'freight.policy.risk'
    _description = 'Policy Risk Details'

    name = fields.Char(string='Title')
    desc = fields.Char(string='Description')