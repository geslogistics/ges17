# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Ticket(models.Model):
    _inherit = 'ticket'
    
    tickt_action_selections = [
  
       
        #Costing Request Selections
        ('req_cost_submit','Submit'),
        ('req_cost_resubmit','Re-Submit'),
        ('req_cost_validate_sale','Validate (Sale)'),
        ('req_cost_cost_item','Cost'),
        ('req_cost_validate_purchase','Validate (Purchase)'),
        ('req_cost_select','Select Cost'),
        ('req_cost_submit_selection','Submit Selection(s)'),
        ('req_cost_confirm_item','Confirm'),
        ('req_cost_bill_item','Bill'),

    ]
    action = fields.Selection(selection_add=tickt_action_selections)
    
    reference_document_selections = [

        ('request.costing', 'Costing Request'),
        ('request.costing.item', 'Costing Request Item'),
 
    ]
    reference_document = fields.Reference(selection_add=reference_document_selections)
    
    request_costing_id = fields.Many2one('request.costing', string="Costing Request")
    request_costing_item_id = fields.Many2one('request.costing.item', string="Costing Request Item")
    