# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PaymentRequestCharges(models.Model):
    _name = 'payment.request.charges'
    _rec_name = 'name'
    _description = 'Payment Request Charges'

    _sql_constraints = [('code', 'unique (code)', 'The code must be unique, this one is already in the system.'),
                        ('name', 'unique (name)', 'The name must be unique, this one is already in the system.')]

    code = fields.Char(string="Code", tracking=True)
    name = fields.Char(string="Name", tracking=True)


class PaymentRequest(models.Model):
    _name = 'payment.request'
    _rec_name = 'name'
    _description = 'Payment Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        """PR Sequence Number"""
        vals['name'] = self.env['ir.sequence'].next_by_code('payment.request.number')
        new_record = super(PaymentRequest, self).create(vals)
        return new_record

    def make_request(self):
        self.ensure_one()
        if self.customs_id:
            if self.customs_id.transport == 'ocean':
                shipment_mode = dict(self.customs_id._fields['ocean_shipment_mode'].selection).get(self.customs_id.ocean_shipment_mode)
            elif self.customs_id.transport == 'air':
                shipment_mode = dict(self.customs_id._fields['air_shipment_mode'].selection).get(self.customs_id.air_shipment_mode)
            elif self.customs_id.transport == 'road':
                shipment_mode = dict(self.customs_id._fields['road_shipment_mode'].selection).get(self.customs_id.road_shipment_mode)
            elif self.customs_id.transport == 'rail':
                shipment_mode = dict(self.customs_id._fields['rail_shipment_mode'].selection).get(self.customs_id.rail_shipment_mode)
            direction = dict(self.customs_id._fields['direction'].selection).get(self.customs_id.direction)
            transport = dict(self.customs_id._fields['transport'].selection).get(self.customs_id.transport)
            commodity_type = dict(self.customs_id._fields['commodity_type'].selection).get(self.customs_id.commodity_type)
            self.write({'partner_id': self.customs_id.partner_id, 'status': 'draft', 'request_date': fields.Datetime.now(),
                        'reference_document': self.customs_id, 'other_reference': "Job No: " +
                                                                                  str(self.customs_id.name) + "\nDirection: " + direction + "\nTransport Via: " + transport + "\nCommodity Type: " + commodity_type + "\nShipment Type: " + shipment_mode, })

    def req_for_approval(self):
        self.ensure_one()
        now = fields.datetime.now()
        values = {'request_for_approval': now, 'status': 'under_review'}
        if self.request_date:
            rd_to_rfa = round((now - fields.Datetime.from_string(self.request_date)).total_seconds() / 60, 2)
            values['rd_to_rfa'] = "{:.2f}".format(rd_to_rfa) + " minute(s)"
        self.write(values)

    def make_approval(self):
        self.ensure_one()
        now = fields.datetime.now()
        values = {'approved_date': now, 'status': 'approved'}
        if self.request_date:
            rd_to_ad = round((now - fields.Datetime.from_string(self.request_date)).total_seconds() / 60, 2)
            values['rd_to_ad'] = "{:.2f}".format(rd_to_ad) + " minute(s)"
        if self.request_for_approval:
            rfa_to_ad = round((now - fields.Datetime.from_string(self.request_for_approval)).total_seconds() / 60, 2)
            values['rfa_to_ad'] = "{:.2f}".format(rfa_to_ad) + " minute(s)"
        self.write(values)

    def make_rejected(self):
        self.ensure_one()
        self.write({'status': 'rejected', 'rejected_date': fields.Datetime.now()})

    def make_paid(self):
        self.ensure_one()
        now = fields.datetime.now()
        values = {'paid_date': now, 'status': 'paid'}
        if self.request_date:
            rd_to_pd = round((now - fields.Datetime.from_string(self.request_date)).total_seconds() / 60, 2)
            values['rd_to_pd'] = "{:.2f}".format(rd_to_pd) + " minute(s)"
        if self.request_for_approval:
            rfa_to_pd = round((now - fields.Datetime.from_string(self.request_for_approval)).total_seconds() / 60, 2)
            values['rfa_to_pd'] = "{:.2f}".format(rfa_to_pd) + " minute(s)"
        if self.approved_date:
            ad_to_pd = round((now - fields.Datetime.from_string(self.approved_date)).total_seconds() / 60, 2)
            values['ad_to_pd'] = "{:.2f}".format(ad_to_pd) + " minute(s)"
        self.write(values)
        if self.reference_document.so_id:
            product_name = "Third Party payments on behalf of client"
            product = self.env['product.template'].search([('name', '=', product_name)], limit=1)
            self.reference_document.so_id.write({
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'name': self.pr_charges_id.name,
                    'price_unit': self.amount,
                    'product_uom_qty': 1,
                    'tax_id': [(6, 0, [])],
                })], })

    name = fields.Char(string="PR", copy=False)
    active = fields.Boolean(default=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency", related='company_id.currency_id')
    partner_id = fields.Many2one(comodel_name='res.partner', tracking=True)
    pr_charges_id = fields.Many2one(comodel_name='payment.request.charges', string="Charges", tracking=True)
    amount = fields.Monetary(string="Amount", required=True, tracking=True, currency_field='company_currency_id')
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment", tracking=True)
    status = fields.Selection(string="Status", tracking=True,
                              selection=[('draft', 'Draft'), ('under_review', 'Under Review'), ('approved', 'Approved'),
                                         ('paid', 'Paid'), ('rejected', 'Rejected'), ])
    other_reference = fields.Text(string="Other Reference", tracking=True)
    reference = fields.Text(string="Reference", tracking=True)
    request_date = fields.Datetime(string="Request Date", tracking=True)
    request_for_approval = fields.Datetime(string="Request For Approval", tracking=True)
    approved_date = fields.Datetime(string="Approved Datetime", tracking=True)
    rejected_date = fields.Datetime(string="Rejected Datetime", tracking=True)
    paid_date = fields.Datetime(string="Paid Datetime", tracking=True)

    rd_to_rfa = fields.Char(string="Request Date to Request for Approval", tracking=True, decimal=2)
    rd_to_ad = fields.Char(string="Request Date to Approved Time Taken", tracking=True)
    rd_to_pd = fields.Char(string="Request Date to Paid Time Taken", tracking=True)

    rfa_to_ad = fields.Char(string="Request for approval to Approval Time Taken", tracking=True)
    rfa_to_pd = fields.Char(string="Request for approval to Paid Time Taken", tracking=True)

    ad_to_pd = fields.Char(string="Approved time to Paid Time Taken")

    # Many2one fields
    customs_id = fields.Many2one(comodel_name='logistics.customs.order', string="Custom Clearance")
    reference_document = fields.Reference(selection=[('logistics.shipment.order', 'Shipment Order'), ('logistics.transport.order', 'Transport Order'),
                                                     ('logistics.storage.order', 'Storage Order'), ('logistics.customs.order', 'Customs Order'),
                                                     ('logistics.service.order', 'Service Order'), ], ondelete='restrict', string="Source Document")
