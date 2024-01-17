# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from pytz import timezone

class Ticket(models.Model):
    _name = 'ticket'
    _description = "Tickets"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "action"
    
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')

    user_id = fields.Many2one('res.users', string='User', no_sort=True)
    requester_user_id = fields.Many2one('res.users', string='User', no_sort=True)

    state = fields.Selection([('open','Open'),('closed','Closed'),('cancel','Cancelled')], string="Status")

    opened_datetime = fields.Datetime(string="Opened On")
    closed_datetime = fields.Datetime(string="Closed On")
    open_duration = fields.Float(string="Open Duration (Hours)", compute="_compute_open_duration")
    
    tickt_action_selections = [
        #Partner Application Selections
        ('created','Created'),
        ('submitted','Submitted'),
        ('resubmitted','Re-Submitted'),
        ('validated','Validated'),
        ('returned','Returned'),
        ('approved','Approved'),
        ('activated','Activated'),
        ('rejected','Rejected'),
        ('pending_validation','Pending Validation'),
        ('pending_approval','Pending Approval'),
        ('validated_by_others','Validated by Others'),
        ('approved_by_others','Approved by Others'),
        ('rejected_by_others','Rejected by Others'),
        ('returned_by_others','Returned by Others'),
        ('cancelled','Cancelled'),
        ('cancelled_by_others','Cancelled by Others'),
        ('expired','Expired'),

        #Partner Application Selections
        ('app_partner_submit','Submit'),
        ('app_partner_resubmit','Re-Submit'),
        ('app_partner_validate_unit','Unit Validate'),
        ('app_partner_validate_function','Function Validate'),
        ('app_partner_approve','Approve'),
        ('app_partner_cancel','Cancel'),

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
    action = fields.Selection(selection=tickt_action_selections, string="Action", no_sort=True)
    
    reference_document_selections = [

        ('request.costing', 'Costing Request'),
        ('request.costing.item', 'Costing Request Item'),
        ('application.partner','Partner Application'),
 
    ]
    reference_document = fields.Reference(selection=reference_document_selections, string="Ref Doc")
    request_costing_id = fields.Many2one('request.costing', string="Costing Request", auto_join=True)
    request_costing_item_id = fields.Many2one('request.costing.item', string="Costing Request Item", auto_join=True)
    app_partner_id = fields.Many2one('application.partner', string="Partner Application", auto_join=True)

    note = fields.Text(string="Notes")

    @api.depends('opened_datetime','closed_datetime')
    def _compute_open_duration(self):
        for record in self:
            record.open_duration = 0
            if record.closed_datetime:
                record.open_duration = (record.closed_datetime - record.opened_datetime).total_seconds() / 60 / 60

    