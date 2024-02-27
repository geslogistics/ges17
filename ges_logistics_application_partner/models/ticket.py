# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Ticket(models.Model):
    _inherit = 'ticket'
    
    tickt_action_selections = [
  
        #Partner Application Selections
        ('app_partner_submit','Submit'),
        ('app_partner_resubmit','Re-Submit'),
        ('app_partner_validate_unit','Unit Validate'),
        ('app_partner_validate_function','Function Validate'),
        ('app_partner_approve','Approve'),
        ('app_partner_cancel','Cancel'),

    ]
    action = fields.Selection(selection_add=tickt_action_selections)
    
    reference_document_selections = [

        ('application.partner','Partner Application'),
 
    ]
    reference_document = fields.Reference(selection_add=reference_document_selections)
    
    app_partner_id = fields.Many2one('application.partner', string="Partner Application")
    