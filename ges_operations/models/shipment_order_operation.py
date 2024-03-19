from odoo import models, fields, api, _

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
import datetime
import pytz

class ShipmentOrderOperation(models.Model):
    _name = "shipment.order.operation"
    _description = "Shipment Order Operation"
    _order = 'type_seq, etd_datetime, sequence'
    _auto = False

    shipment_order_id = fields.Many2one('shipment.order', string="Shipment Order", ondelete="cascade")
    operation_type = fields.Selection([('route','Route'),('service','Service')], string="Type")
    
    #routes
    route_id = fields.Many2one('shipment.order.route', string="Route", ondelete="cascade", auto_join=True)
    sequence = fields.Integer(string="Sequence", related="route_id.sequence")
    route_type = fields.Selection(([('main-carriage', 'Main-Carriage'),('pre-carriage', 'Pre-Carriage'), ('on-carriage', 'On-Carriage')]), string='Route Type', related="route_id.route_type")
    type_seq = fields.Integer()

    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', related="route_id.transport")

    #origin fields
    origin_address_type = fields.Selection([('port','Port'),('location','Location')], related="route_id.origin_address_type")
    origin_port_id = fields.Many2one('freight.port', string="Loading Port", related="route_id.origin_port_id")
    origin_address_id = fields.Many2one('freight.address', string="Loading Location", related="route_id.origin_address_id")
    origin_country_id = fields.Many2one('res.country', string="Loading Country", related="route_id.origin_country_id")
    origin_state_id = fields.Many2one('res.country.state', string="Loading State", related="route_id.origin_state_id")
    origin_city_id = fields.Many2one('res.city', string="Loading City", related="route_id.origin_city_id")
    origin_zip_code = fields.Char(string="Loading Zip Code", related="route_id.origin_zip_code")
    origin_street = fields.Char(string="Loading Street 1", related="route_id.origin_street")
    origin_street2 = fields.Char(string="Loading Street 2", related="route_id.origin_street2")
    origin_code = fields.Char(string="Loading Address Code", related="route_id.origin_code")

    
    #destination fields
    destination_address_type = fields.Selection([('port','Port'),('location','Location')], related="route_id.destination_address_type")
    destination_port_id = fields.Many2one('freight.port', string="Discharge Port", related="route_id.destination_port_id")
    destination_address_id = fields.Many2one('freight.address', string="Discharge Location", related="route_id.destination_address_id")
    destination_country_id = fields.Many2one('res.country', string="Discharge Country", related="route_id.destination_country_id")
    destination_state_id = fields.Many2one('res.country.state', string="Discharge State", related="route_id.destination_state_id")
    destination_city_id = fields.Many2one('res.city', string="Discharge City", related="route_id.destination_city_id")
    destination_zip_code = fields.Char(string="Discharge Zip Code", related="route_id.destination_zip_code")
    destination_street = fields.Char(string="Discharge Street 1", related="route_id.destination_street")
    destination_street2 = fields.Char(string="Discharge Street 2", related="route_id.destination_street2")
    destination_code = fields.Char(string="Discharge Address Code", related="route_id.destination_code")


    # Carriage Dates
    etd_datetime = fields.Datetime('ETD Date', help="Estimated Date/Time of Departure", related="route_id.etd_datetime")
    atd_datetime = fields.Datetime('ATD Date', help="Actual Date/Time of Departure", related="route_id.atd_datetime")
    eta_datetime = fields.Datetime('ETA Date', help="Estimated Date/Time of Arrival", related="route_id.eta_datetime")
    ata_datetime = fields.Datetime('ATA Date', help="Actual Date/Time of Arrival", related="route_id.ata_datetime")

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
            

    def init(self):
        tools.drop_view_if_exists(self._cr, 'shipment_order_operation')
        self._cr.execute(""" 
        CREATE OR REPLACE VIEW shipment_order_operation AS ( 
                SELECT 
                row_number() OVER() as id,
                shr.shipment_order_id as shipment_order_id,                
                shr.route_type as route_type,            
                shr.transport as transport,
                'route' as operation_type,
                shr.id as route_id,
                shr.type_seq as type_seq
                FROM shipment_order_route shr)
            """)

    def open_record(self):
        if self.operation_type == 'route':
            return {
                'type': 'ir.actions.act_window', 
                'res_model': 'shipment.order.route', 
                'name': self.route_id.display_name, 
                'view_type': 'form', 
                'view_mode': 'form', 
                'res_id': self.route_id.id, 
                'target': 'new', 
            }
        