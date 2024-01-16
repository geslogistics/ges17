# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import re

_logger = logging.getLogger(__name__)


class TransportOrder(models.Model):
    _name = "logistics.transport.order"
    _description = "Transportation Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency", related='company_id.currency_id')

    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    priority = fields.Selection([('0', 'Low priority'), ('1', 'Medium priority'), ('2', 'High priority'), ('3', 'Urgent')], string='Priority',
                                tracking=True, index=True)
    delivery_date = fields.Date(string='Delivery Date', tracking=True, required=True)
    port_id = fields.Many2one(comodel_name='logistics.freight.port', string='Port', tracking=True)

    direction = fields.Selection(string="Direction", selection=[('import', 'Import'), ('export', 'Export')], required=True, tracking=True)
    shipment_type_id = fields.Many2one(comodel_name='logistics.product.shipment.type', string='Shipment Type', required=True, tracking=True)

    # linkage / creation fields
    source_sol_id = fields.Many2one('sale.order.line', string="Source SOL", store=False)
    
    # Services Required
    make_pullout = fields.Boolean(string='Make Pullout', tracking=True)
    make_repullout = fields.Boolean(string='Make Re - Pullout', tracking=True)
    make_empty_collection = fields.Boolean(string='Empty Collection', tracking=True)
    make_empty_return_collection = fields.Boolean(string='Empty Return Collection', tracking=True)
    breakdown = fields.Boolean(string='Breakdown', tracking=True)

    # Transport Information
    transportation_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    container_number = fields.Char(string='Container Number', required=True)
    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True)
    fleet_name = fields.Char("Fleet", tracking=True)
    driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    driver_name = fields.Char("Driver", tracking=True)
    driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)

    loading_city_id = fields.Many2one('logistics.freight.address.city', string="From", tracking=True)
    destination_city_id = fields.Many2one('logistics.freight.address.city', string="To", tracking=True)
    fleet_type = fields.Char(string='Fleet Type', tracking=True)
    origin_loading_date = fields.Date(string='Origin Loading Date', tracking=True)
    destination_arrival_date = fields.Date(string="Destination Arrival Date", tracking=True)
    return_date = fields.Date(string="Return Date", tracking=True)
    stuffing_date = fields.Date(string='Stuffing Date', tracking=True)
    waybill_date = fields.Date(string='Waybill Date', tracking=True)
    pod_date = fields.Date(string="POD Date", tracking=True)

    receiver_name = fields.Char(string="Receiver Name", tracking=True)
    receiver_contact = fields.Char(string="Receiver Contact Information", tracking=True)

    # PullOut Information
    pullout_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    pullout_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    pullout_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True)
    pullout_fleet_name = fields.Char("Fleet", tracking=True)
    pullout_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    pullout_driver_name = fields.Char("Driver", tracking=True)
    pullout_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    pullout_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    pullout_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                      string="PullOut Status", tracking=True)
    pullout_schedule_date = fields.Date(string='Pull Out Schedule Date', tracking=True)
    pullout_complete_date = fields.Date(string='Pull Out Complete Date', tracking=True)
    pullout_type = fields.Selection(string='Pullout Type', selection=[('self', 'Self'), ('customer', 'Customer'), ], tracking=True)
    self_pullout_reason = fields.Text(string='Self Pull Out Reason', tracking=True)
    pullout_port_id = fields.Many2one(comodel_name='logistics.freight.port', string='From Site', tracking=True)

    # Empty Collection
    empty_collection_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Collection Mode",
                                             tracking=True)
    empty_collection_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    empty_collection_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True)
    empty_collection_fleet_name = fields.Char("Fleet", tracking=True)
    empty_collection_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    empty_collection_driver_name = fields.Char("Driver", tracking=True)
    empty_collection_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    empty_collection_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    empty_collection_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                               string="Empty Collection Status", tracking=True)
    empty_collection_scheduled_date = fields.Date(string='Empty Collection Scheduled Date', tracking=True)
    empty_collection_date = fields.Date(string='Empty Collection Complete Date', tracking=True)

    # Empty Return Collection
    erc_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    erc_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    erc_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True)
    erc_fleet_name = fields.Char("Fleet", tracking=True)
    erc_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    erc_driver_name = fields.Char("Driver", tracking=True)
    erc_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    erc_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    erc_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                  string="Empty Return Collection Status", tracking=True)
    erc_scheduled_date = fields.Date(string='Empty Return Collection Complete Date', tracking=True)
    erc_date = fields.Date(string='Empty Return Collection Complete Date', tracking=True)

    @api.onchange('container_number')
    def container_number_check_onchange(self):
        for rec in self:
            if rec.container_number:
                if len(rec.container_number) > 11:
                    raise ValidationError(
                        f"The container number exceeds the maximum length (11 characters): {rec.container_number}"
                    )
                if not re.match('^[A-Z]{4}[0-9]{7,}$', rec.container_number.upper()):
                    raise ValidationError(
                        f"You have Entered a Wrong Container Number or Format: {rec.container_number.upper()}\n"
                        "Format is ABCD1234567\n"
                        "First Four Characters Must be Alphabet and Last Seven Characters Must be Numeric"
                    )
                rec.container_number = rec.container_number.upper()

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.fleet_id:
            self.fleet_name = self.fleet_id.display_name
            driver = self.fleet_id.driver_id
            if driver:
                self.driver_id = driver.id
                self.driver_name = driver.name
                self.driver_mobile_number = driver.mobile

    def pullout_trip(self):
        self.write({'pullout_status': 'inprogress'})

    def pullout_completed(self):
        self.write({
            'pullout_complete_date': fields.Date.today(),
            'pullout_status': 'finished'
        })

    def ec_trip(self):
        self.write({'empty_collection_status': 'inprogress'})

    def ec_completed(self):
        self.write({
            'empty_collection_date': fields.Date.today(),
            'empty_collection_status': 'finished'
        })

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.fleet_id:
            self.fleet_name = self.fleet_id.display_name
            driver = self.fleet_id.driver_id
            if driver:
                self.driver_id = driver.id
                self.driver_name = driver.name
                self.driver_mobile_number = driver.mobile
