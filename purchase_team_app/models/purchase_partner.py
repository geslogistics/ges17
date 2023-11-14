# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartnerInherit(models.Model):
	_inherit = 'res.partner'

	purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")
	purchase_user_id = fields.Many2one('res.users', string="Purchase User")






class ResUsers(models.Model):
    _inherit = 'res.users'

    
    purchase_team_id = fields.Many2one('purchase.team', string='User Purchase Team', store=True, help="Main user purchase team.")
