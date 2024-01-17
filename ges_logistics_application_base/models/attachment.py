# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ApplicationAttachment(models.Model):
    _name = 'application.attachment'
    _description = "Application Attachments"
    _order = 'create_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("Name")
    attachment_type_id = fields.Many2one('application.attachment.type', string="Attachment Type")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    application_id = fields.Many2one('application.partner', string="Application")

class ApplicationAttachmentTypes(models.Model):
    _name = 'application.attachment.type'
    _description = "Application Attachment Types"
    _order = 'sequence, id desc'
    
    sequence = fields.Integer("Sequence")
    name = fields.Char("Name")
