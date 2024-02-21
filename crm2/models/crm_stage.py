# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json
from lxml import etree

class Stage(models.Model):
    _inherit = 'crm.stage'

    ou_id = fields.Many2one('operating.unit', string='Unit', ondelete="set null",
        help='Specific unit that uses this stage. Other units will not be able to see or use this stage.')

    
