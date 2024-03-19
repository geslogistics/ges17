# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ApplicationAttachment(models.Model):
    _inherit = 'application.attachment'
    application_id = fields.Many2one('application.partner', string="Application")
