# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'

	purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")
	purchase_user_id = fields.Many2one('res.users', string="Purchase User")
