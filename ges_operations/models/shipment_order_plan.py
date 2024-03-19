# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import datetime
import pytz

class ShipmentOrderPlan(models.Model):
    _name = "shipment.order.plan"
    _description = "Shipment Order Plan"
    _order = "etd_datetime, sequence"

    shipment_order_id = fields.Many2one('shipment.order', string="Shipment Order", ondelete="cascade")
    partner_id = fields.Many2one('res.partner',related="shipment_order_id.partner_id")
    
    company_id = fields.Many2one(string="Company", related="shipment_order_id.company_id")
    currency_id = fields.Many2one(string="Currency", related="shipment_order_id.currency_id")

    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string="Color", related="shipment_order_id.color")
    sequence = fields.Integer(string="Sequence")
    
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())

    # general order fields
    operation_type = fields.Selection([('leg','Route'),('service','Service')], string="Type")
    route_id = fields.Many2one('shipment.order.route', string="Route", ondelete="cascade", auto_join=True)
    service_id = fields.Many2one('shipment.order.service', string="Service", ondelete="cascade")
    route_type = fields.Selection(([('main-carriage', 'Main-Carriage'),('pre-carriage', 'Pre-Carriage'), ('on-carriage', 'On-Carriage')]), string='Route Type', default="pre-carriage")
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', default="ocean")
    child_plan_ids = fields.One2many('shipment.order.plan', 'parent_plan_id', string="Child Plans")
    count_child_plans = fields.Integer(string="Count", compute="_compute_count_child_plans")

    @api.depends('count_child_plans')
    @api.onchange('count_child_plans')
    def _compute_count_child_plans(self):
        for record in self:
            record.count_child_plans = 1+ len(record.child_plan_ids)


    parent_plan_id = fields.Many2one('shipment.order.plan', string="Parent Plan", ondelete="cascade")

    #origin fields
    origin_address_type = fields.Selection([('port','Port'),('location','Location')])
    origin_port_id = fields.Many2one('freight.port', string="Loading Port")
    origin_address_id = fields.Many2one('freight.address', string="Loading Location")
    origin_country_id = fields.Many2one('res.country', string="Loading Country", compute="_compute_origin_address", store=True, copy=False)
    origin_state_id = fields.Many2one('res.country.state', string="Loading State", compute="_compute_origin_address", store=True, copy=False)
    origin_city_id = fields.Many2one('res.city', string="Loading City", compute="_compute_origin_address", store=True, copy=False)
    origin_zip_code = fields.Char(string="Loading Zip Code", compute="_compute_origin_address", store=True, copy=False)
    origin_street = fields.Char(string="Loading Street 1", compute="_compute_origin_address", store=True, copy=False)
    origin_street2 = fields.Char(string="Loading Street 2", compute="_compute_origin_address", store=True, copy=False)
    origin_code = fields.Char(string="Loading Address Code", compute="_compute_origin_address", store=True, copy=False)

    @api.depends('origin_address_type')
    @api.onchange('origin_address_type')
    def _reset_origin_address(self):
        for record in self:
            if record.origin_address_type == 'port':
                record.origin_address_id = False
            elif record.origin_address_type == 'location':
                record.origin_port_id = False

    @api.depends('origin_address_type','origin_port_id','origin_address_id')
    @api.onchange('origin_address_type','origin_port_id','origin_address_id')
    def _compute_origin_address(self):
        for record in self:
            record.origin_country_id = False
            record.origin_state_id = False
            record.origin_city_id = False
            record.origin_zip_code = False
            record.origin_street = False
            record.origin_street2 = False
            record.origin_code = False

            if record.origin_address_type == 'port':
                if record.origin_port_id:
                    record.origin_country_id = record.origin_port_id.country_id
                    record.origin_state_id = record.origin_port_id.state_id
                    record.origin_city_id = record.origin_port_id.city_id
                    record.origin_zip_code = record.origin_port_id.zip_code
                    record.origin_street = record.origin_port_id.street
                    record.origin_street2 = record.origin_port_id.street2
                    record.origin_code = record.origin_port_id.code

            elif record.origin_address_type == 'location':
                if record.origin_address_id:
                    record.origin_country_id = record.origin_address_id.country_id
                    record.origin_state_id = record.origin_address_id.state_id
                    record.origin_city_id = record.origin_address_id.city_id
                    record.origin_zip_code = record.origin_address_id.zip_code
                    record.origin_street = record.origin_address_id.street
                    record.origin_street2 = record.origin_address_id.street2
                    record.origin_code = record.origin_address_id.code

    #destination fields
    destination_address_type = fields.Selection([('port','Port'),('location','Location')])
    destination_port_id = fields.Many2one('freight.port', string="Discharge Port")
    destination_address_id = fields.Many2one('freight.address', string="Discharge Location")
    destination_country_id = fields.Many2one('res.country', string="Discharge Country", compute="_compute_destination_address", store=True, copy=False)
    destination_state_id = fields.Many2one('res.country.state', string="Discharge State", compute="_compute_destination_address", store=True, copy=False)
    destination_city_id = fields.Many2one('res.city', string="Discharge City", compute="_compute_destination_address", store=True, copy=False)
    destination_zip_code = fields.Char(string="Discharge Zip Code", compute="_compute_destination_address", store=True, copy=False)
    destination_street = fields.Char(string="Discharge Street 1", compute="_compute_destination_address", store=True, copy=False)
    destination_street2 = fields.Char(string="Discharge Street 2", compute="_compute_destination_address", store=True, copy=False)
    destination_code = fields.Char(string="Discharge Address Code", compute="_compute_destination_address", store=True, copy=False)


    @api.depends('destination_address_type')
    @api.onchange('destination_address_type')
    def _reset_destination_address(self):
        for record in self:
            if record.destination_address_type == 'port':
                record.destination_address_id = False
            elif record.destination_address_type == 'location':
                record.destination_port_id = False

    @api.depends('destination_address_type','destination_port_id','destination_address_id')
    @api.onchange('destination_address_type','destination_port_id','destination_address_id')
    def _compute_destination_address(self):
        for record in self:
            record.destination_country_id = False
            record.destination_state_id = False
            record.destination_city_id = False
            record.destination_zip_code = False
            record.destination_street = False
            record.destination_street2 = False
            record.destination_code = False

            if record.destination_address_type == 'port':
                if record.destination_port_id:
                    record.destination_country_id = record.destination_port_id.country_id
                    record.destination_state_id = record.destination_port_id.state_id
                    record.destination_city_id = record.destination_port_id.city_id
                    record.destination_zip_code = record.destination_port_id.zip_code
                    record.destination_street = record.destination_port_id.street
                    record.destination_street2 = record.destination_port_id.street2
                    record.destination_code = record.destination_port_id.code

            elif record.destination_address_type == 'location':
                if record.destination_address_id:
                    record.destination_country_id = record.destination_address_id.country_id
                    record.destination_state_id = record.destination_address_id.state_id
                    record.destination_city_id = record.destination_address_id.city_id
                    record.destination_zip_code = record.destination_address_id.zip_code
                    record.destination_street = record.destination_address_id.street
                    record.destination_street2 = record.destination_address_id.street2
                    record.destination_code = record.destination_address_id.code


    # Carriage Dates
    etd_datetime = fields.Datetime('ETD Date', help="Estimated Date/Time of Departure")
    atd_datetime = fields.Datetime('ATD Date', help="Actual Date/Time of Departure")
    eta_datetime = fields.Datetime('ETA Date', help="Estimated Date/Time of Arrival")
    ata_datetime = fields.Datetime('ATA Date', help="Actual Date/Time of Arrival")

    etd_date = fields.Date('ETD Date', help="Estimated Date of Departure", compute="_compute_etas")
    atd_date = fields.Date('ATD Date', help="Actual Date of Departure", compute="_compute_etas")
    eta_date = fields.Date('ETA Date', help="Estimated Date of Arrival", compute="_compute_etas")
    ata_date = fields.Date('ATA Date', help="Actual Date of Arrival", compute="_compute_etas")


    @api.depends('etd_datetime','atd_datetime','eta_datetime','ata_datetime')
    @api.onchange('etd_date','atd_date','eta_date','ata_date','etd_time','atd_time','eta_time','ata_time')
    def _compute_etas(self):
        for record in self:  
            record.etd_date = record.etd_datetime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(record.env.user.tz)).replace(tzinfo=None).date() if record.etd_datetime else False
            record.atd_date = record.etd_datetime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(record.env.user.tz)).replace(tzinfo=None).date() if record.atd_datetime else False
            record.eta_date = record.eta_datetime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(record.env.user.tz)).replace(tzinfo=None).date() if record.eta_datetime else False
            record.ata_date = record.ata_datetime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(record.env.user.tz)).replace(tzinfo=None).date() if record.ata_datetime else False
            

    