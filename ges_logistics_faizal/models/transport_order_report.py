# -*- coding: utf-8 -*-
from odoo import models, api, tools, fields, SUPERUSER_ID, _


class TransportOrderReport(models.Model):
    _name = 'transport.order.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Transport Orders Report"
    _order = 'creation_date desc'
    _rec_name = 'transport_order_id'

    fleet_id = fields.Many2one(comodel_name='fleet.vehicle', string='Fleet', tracking=True)
    fleet_name = fields.Char(string='Fleet', tracking=True)
    driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    driver_name = fields.Char(string='Driver', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    trip_type = fields.Selection(string='Trip Type', selection=[('pullout', 'Pullout'), ('shuttling', 'Shuttling'), ('empty_return', 'Empty Return'),
                                                                ('empty_pickup', 'Empty Pickup'),
                                                                ('customer_transportation', 'Customer Transportation')], tracking=True)
    transportation_mode = fields.Selection(string='Transportation Mode', selection=[('internal', 'Internal'), ('external', 'External')],
                                           tracking=True)
    creation_date = fields.Datetime(string='Creation Date', tracking=True)
    finished_date = fields.Datetime(string='Finished Date', tracking=True)
    direction = fields.Selection(string='Direction', selection=[('import', 'Import'), ('export', 'Export')], tracking=True)
    cargo_type = fields.Selection(string='Cargo Type', selection=[('ltl', 'LTL'), ('ftl', 'FTL')])
    shipment_mode = fields.Selection([('full_truck_load_ftl_flatbed_trailer', 'Full Truck Load (FTL) > Flatbed Trailer'),
                                      ('full_truck_load_ftl_lowbed_trailer', 'Full Truck Load (FTL) > Lowbed Trailer'),
                                      ('full_truck_load_ftl_self-propelled_modular_transporter_spmt',
                                       'Full Truck Load (FTL) > Self-Propelled Modular Transporter (SPMT)'),
                                      ('full_truck_load_ftl_car_carrier', 'Full Truck Load (FTL) > Car Carrier'),
                                      ('full_truck_load_ftl_temperature_controlled', 'Full Truck Load (FTL) > Temperature Controlled'),
                                      ('full_truck_load_ftl_liquid_tank', 'Full Truck Load (FTL) > Liquid Tank'),
                                      ('full_truck_load_ftl_dyna/lorry', 'Full Truck Load (FTL) > Dyna/Lorry'),
                                      ('less_than_truck_load_ltl_flatbed_trailer', 'Less Than Truck Load (LTL) > Flatbed Trailer'),
                                      ('less_than_truck_load_ltl_lowbed_trailer', 'Less Than Truck Load (LTL) > Lowbed Trailer'),
                                      ('less_than_truck_load_ltl_temperature_controlled', 'Less Than Truck Load (LTL) > Temperature Controlled'),
                                      ('less_than_truck_load_ltl_dyna/lorry', 'Less Than Truck Load (LTL) > Dyna/Lorry'), ('others', 'Others'), ],
                                     string='Shipment Type', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    trip_money = fields.Monetary(string='Trip Money', currency_field='currency_id', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    origin_address_id = fields.Many2one('logistics.freight.address', string='Origin Address', ondelete='restrict', tracking=True)
    destination_address_id = fields.Many2one('logistics.freight.address', string='Destination Address', ondelete='restrict', tracking=True)
    status = fields.Selection(selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('finished', 'Finished'), ('cancelled', 'Cancelled')],
                              string='Status', tracking=True)
    transport_order_id = fields.Many2one('logistics.transport.order', string='Transport Order', tracking=True)
