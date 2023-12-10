# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from pytz import timezone

class Ticket(models.Model):
    _name = 'ticket'
    _description = "Tickets"
    
    user_id = fields.Many2one('res.users', string='User', no_sort=True)
    tickt_action_selections = [
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
    ]
    action = fields.Selection(selection=tickt_action_selections, string="Action", no_sort=True)
    action_datetime = fields.Datetime(string="Timestamp", default=fields.Datetime.now(), no_sort=True)
    pending_timestamp = fields.Datetime(string="Pending Timestamp", no_sort=True)
    pending_time = fields.Float(string="Pending Hours", compute="_compute_pending_time", no_sort=True)
    
    reference_document_selections = [
        ('logistics.shipment.order', 'Shipment Order'),
        ('logistics.transport.order', 'Transport Order'),
        ('logistics.storage.order', 'Storage Order'),
        ('logistics.customs.order', 'Customs Order'),
        ('logistics.service.order', 'Service Order'),
        ('costing.memo', 'Costing Memo'),
        ('pricing.memo', 'Pricing Memo'),
    ]
    reference_document = fields.Reference(selection=reference_document_selections, string="Ref Doc", tracking=True)

    note = fields.Text(string="Notes")

    @api.depends('action_datetime','pending_timestamp')
    def _compute_pending_time(self):
        for record in self:
            record.pending_time = False
            if record.pending_timestamp:
                record.pending_time = (record.action_datetime - record.pending_timestamp).total_seconds() / 60 / 60

    