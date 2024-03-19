# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import re
import uuid

_logger = logging.getLogger(__name__)


class TransportOrder(models.Model):
    _name = "logistics.transport.order"
    _description = "Transportation Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))

    source_ids = fields.Reference(selection=[('logistics.shipment.order', 'Shipment Order'), ('logistics.transport.order', 'Transport Order'),
                                             ('logistics.storage.order', 'Storage Order'), ('logistics.customs.order', 'Customs Order'),
                                             ('logistics.service.order', 'Service Order'), ('sale.order', 'Sale Order')], ondelete='restrict',
                                  string="Source")

    barcode = fields.Char(string="Barcode", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency", related='company_id.currency_id')
    state = fields.Selection([('draft', 'Draft'), ('order_received', 'Order Received'), ('container_pulled_out', 'Container Pulled Out'),
                              ('container_picked_up', 'Container Picked Up'), ('in_transit', 'In Transit'), ('received_pod', 'Received POD'),
                              ('received_pol', 'Received POL'), ('received_eir', 'Received EIR'), ('port_shuttling', 'Port Shuttling'),
                              ('delivery_completed', 'Delivery Completed'), ('delivered_to_port', 'Delivered to Port')], default='draft')

    partner_id = fields.Many2one('res.partner', string="Customer", tracking=True)
    priority = fields.Selection([('0', 'Low priority'), ('1', 'Medium priority'), ('2', 'High priority'), ('3', 'Urgent')], string='Priority',
                                tracking=True, index=True)
    delivery_date_scheduled = fields.Date(string='Delivery Date Scheduled', tracking=True)
    cro_booking_date = fields.Date(string='CRO Booking Date', tracking=True)
    direction = fields.Selection(string="Direction", selection=[('import', 'Import'), ('export', 'Export')], tracking=True)
    cargo_type = fields.Selection(string="Cargo Type", selection=[('ltl', 'LTL'), ('ftl', 'FTL')])
    ltl_shipment_mode = fields.Selection([
        ('less_than_truck_load_ltl_flatbed_trailer', 'Less Than Truck Load (LTL) > Flatbed Trailer'),
        ('less_than_truck_load_ltl_lowbed_trailer', 'Less Than Truck Load (LTL) > Lowbed Trailer'),
        ('less_than_truck_load_ltl_temperature_controlled', 'Less Than Truck Load (LTL) > Temperature Controlled'),
        ('less_than_truck_load_ltl_dyna/lorry', 'Less Than Truck Load (LTL) > Dyna/Lorry'), ('others', 'Others')],
        string="Shipment Type", tracking=True)
    ftl_shipment_mode = fields.Selection([
        ('full_truck_load_ftl_flatbed_trailer', 'Full Truck Load (FTL) > Flatbed Trailer'),
        ('full_truck_load_ftl_lowbed_trailer', 'Full Truck Load (FTL) > Lowbed Trailer'),
        ('full_truck_load_ftl_self-propelled_modular_transporter_spmt', 'Full Truck Load (FTL) > Self-Propelled Modular Transporter (SPMT)'),
        ('full_truck_load_ftl_car_carrier', 'Full Truck Load (FTL) > Car Carrier'),
        ('full_truck_load_ftl_temperature_controlled', 'Full Truck Load (FTL) > Temperature Controlled'),
        ('full_truck_load_ftl_liquid_tank', 'Full Truck Load (FTL) > Liquid Tank'),
        ('full_truck_load_ftl_dyna/lorry', 'Full Truck Load (FTL) > Dyna/Lorry'),
        ('others', 'Others')], string="Shipment Type", tracking=True)
    shipment_mode = fields.Selection([
        ('full_truck_load_ftl_flatbed_trailer', 'Full Truck Load (FTL) > Flatbed Trailer'),
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
        ('less_than_truck_load_ltl_dyna/lorry', 'Less Than Truck Load (LTL) > Dyna/Lorry'),
        ('others', 'Others'), ], string="Shipment Type", tracking=True)
    customer_reference = fields.Char(string="Customer Reference", tracking=True)

    # Services Required
    make_pullout = fields.Boolean(string='Make Pullout', tracking=True)
    make_empty_pickup = fields.Boolean(string='Empty Pickup', tracking=True)
    make_empty_return = fields.Boolean(string='Empty Return', tracking=True)
    breakdown = fields.Boolean(string='Breakdown', tracking=True)
    shuttling = fields.Boolean(string='Shuttling', tracking=True)

    # Transport Information
    transportation_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    container_number = fields.Char(string='Container Number')
    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True, domain=[('truck_current_status', '=', 'idle')])
    fleet_name = fields.Char("Fleet", tracking=True)
    driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    driver_name = fields.Char("Driver", tracking=True)
    driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)

    loading_country_id = fields.Many2one('logistics.freight.address.country', string="Country", ondelete='restrict', tracking=True)
    loading_address_id = fields.Many2one('logistics.freight.address', string="Named Address", ondelete='restrict', tracking=True,
                                         domain="[('country_id', '=', loading_country_id)]")
    loading_address_name = fields.Char(string="Address Name", tracking=True)
    loading_address_code = fields.Char(string="Address Code", tracking=True)
    loading_state_id = fields.Many2one('logistics.freight.address.state', string="State", domain="[('country_id', '=', loading_country_id)]",
                                       tracking=True)
    loading_city_id = fields.Many2one('logistics.freight.address.city', string="City", domain="[('country_id', '=', loading_country_id)]",
                                      tracking=True)
    loading_zipcode = fields.Char(string="Zip Code", tracking=True)
    loading_street = fields.Char(string="Street", tracking=True)
    loading_street2 = fields.Char(string="Street 2", tracking=True)
    loading_street3 = fields.Char(string="Street 3", tracking=True)
    loading_location_map_url = fields.Char(string="Loading Location URL", tracking=True)
    loading_address_save_option = fields.Boolean(string="Save Address", tracking=True)

    destination_country_id = fields.Many2one('logistics.freight.address.country', string="Country", ondelete='restrict', tracking=True)
    destination_address_id = fields.Many2one('logistics.freight.address', string="Named Address",
                                             domain="[('country_id', '=', destination_country_id)]", ondelete='restrict', tracking=True)
    destination_address_name = fields.Char(string="Address Name", tracking=True)
    destination_address_code = fields.Char(string="Address Code", tracking=True)
    destination_state_id = fields.Many2one('logistics.freight.address.state', string="State", domain="[('country_id', '=', destination_country_id)]",
                                           tracking=True)
    destination_city_id = fields.Many2one('logistics.freight.address.city', string="City", domain="[('country_id', '=', destination_country_id)]",
                                          tracking=True)
    destination_zipcode = fields.Char(string="Zip Code", tracking=True)
    destination_street = fields.Char("Street", tracking=True)
    destination_street2 = fields.Char("Street 2", tracking=True)
    destination_street3 = fields.Char("Street 3", tracking=True)
    destination_location_map_url = fields.Char(string="Destination Location URL", tracking=True)
    destination_address_save_option = fields.Boolean(string="Save Address", tracking=True)

    fleet_type = fields.Char(string='Fleet Type', tracking=True)
    container_cleared_date = fields.Date(string='Container Cleared Date', tracking=True)
    destination_arrival_date = fields.Date(string="Destination Arrival Date", tracking=True)
    return_date = fields.Date(string="Return Date", tracking=True)
    stuffing_date = fields.Date(string='Stuffing Date', tracking=True)
    waybill_date = fields.Date(string='Waybill Date', tracking=True)
    pod_date = fields.Date(string="POD Date", tracking=True)
    pol_date = fields.Date(string='POL Date', tracking=True)
    receiver_name = fields.Char(string="Receiver Name", tracking=True)
    receiver_contact = fields.Char(string="Receiver Contact Information", tracking=True)

    # PullOut Information
    pullout_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    pullout_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    pullout_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True, domain=[('truck_current_status', '=', 'idle')])
    pullout_fleet_name = fields.Char("Fleet", tracking=True)
    pullout_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    pullout_driver_name = fields.Char("Driver", tracking=True)
    pullout_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    pullout_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    pullout_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                      string="PullOut Status", tracking=True)
    pullout_schedule_date = fields.Date(string='Pull Out Schedule Date', tracking=True)
    pullout_complete_date = fields.Date(string='Pull Out Complete Date', tracking=True)
    pullout_port_id = fields.Many2one(comodel_name='logistics.freight.port', string='From Site', tracking=True)

    # Empty Pickup
    empty_pickup_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Pickup Mode", tracking=True)
    empty_pickup_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    empty_pickup_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True, domain=[('truck_current_status', '=', 'idle')])
    empty_pickup_fleet_name = fields.Char("Fleet", tracking=True)
    empty_pickup_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    empty_pickup_driver_name = fields.Char("Driver", tracking=True)
    empty_pickup_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    empty_pickup_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    empty_pickup_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                           string="Empty Pickup Status", tracking=True)
    empty_pickup_scheduled_date = fields.Date(string='Empty Pickup Scheduled Date', tracking=True)
    empty_pickup_date = fields.Date(string='Empty Pickup Complete Date', tracking=True)

    # Empty Return
    er_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    er_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    er_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True, domain=[('truck_current_status', '=', 'idle')])
    er_fleet_name = fields.Char("Fleet", tracking=True)
    er_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    er_driver_name = fields.Char("Driver", tracking=True)
    er_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    er_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    er_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                 string="Empty Return Collection Status", tracking=True)
    er_scheduled_date = fields.Date(string='Empty Return Collection Complete Date', tracking=True)
    er_date = fields.Date(string='Empty Return Collection Complete Date', tracking=True)

    # Shuttling Details
    shuttling_mode = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Transportation Mode", tracking=True)
    shuttling_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    shuttling_fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True, domain=[('truck_current_status', '=', 'idle')])
    shuttling_fleet_name = fields.Char("Fleet", tracking=True)
    shuttling_driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    shuttling_driver_name = fields.Char("Driver", tracking=True)
    shuttling_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    shuttling_trip_money_vendor_charges = fields.Monetary(currency_field='company_currency_id', string="Charges", tracking=True)
    shuttling_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('finished', 'Finished')], default='draft',
                                        string="PullOut Status", tracking=True)
    shuttling_schedule_date = fields.Date(string='Shuttling Schedule Date', tracking=True)
    shuttling_complete_date = fields.Date(string='Shuttling Complete Date', tracking=True)
    shuttling_port_id = fields.Many2one(comodel_name='logistics.freight.port', string='From Site', tracking=True)

    # Break Down Details
    breakdown_mode = fields.Selection(string="Breakdown Mode", selection=[('internal', 'Internal'), ('external', 'External')], tracking=True)
    breakdown_fleet_id = fields.Many2one(comodel_name='fleet.vehicle', string="Fleet", tracking=True)
    breakdown_fleet = fields.Char(string="Fleet", tracking=True)
    breakdown_driver_id = fields.Many2one(comodel_name='res.partner', string="Driver", tracking=True)
    breakdown_vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", tracking=True)
    breakdown_driver = fields.Char(string="Driver", tracking=True)
    breakdown_driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    breakdown_location = fields.Char(string="Breakdown Location", tracking=True)
    breakdown_remarks = fields.Text(string="Remarks", tracking=True)
    breakdown_trip_money = fields.Monetary(string="Breakdown Trip Money", currency_field='company_currency_id', tracking=True)
    breakdown_date = fields.Datetime(string="Breakdown Datetime", tracking=True)
    breakdown_status = fields.Selection([('breakdown', 'Breakdown'), ('inprogress', 'In Progress'), ('finished', 'Breakdown Finished')],
                                        string="Breakdown Status", tracking=True)

    # One2many Fields
    transport_cost_ids = fields.One2many('logistics.transport.cost', 'transport_id', string="Costs")

    # Create function
    @api.model
    def create(self, vals):
        if vals.get('loading_address_save_option') and not vals.get('loading_address_id'):
            logistics_address = self.env['logistics.freight.address'].create(
                {'name': vals.get('loading_address_name'), 'code': vals.get('loading_address_code'), 'state_id': vals.get('loading_state_id'),
                 'city_id': vals.get('loading_city_id'), 'zip_code': vals.get('loading_zipcode'), 'street': vals.get('loading_street'),
                 'street2': vals.get('loading_street2'), 'street3': vals.get('loading_street3'), 'country_id': vals.get('loading_country_id'),
                 'location_url': vals.get('loading_location_map_url')})
            vals['loading_address_id'] = logistics_address.id

        if vals.get('destination_address_save_option') and not vals.get('destination_address_id'):
            logistics_address = self.env['logistics.freight.address'].create(
                {'name': vals.get('destination_address_name'), 'code': vals.get('destination_address_code'),
                 'state_id': vals.get('destination_state_id'), 'city_id': vals.get('destination_city_id'),
                 'zip_code': vals.get('destination_zipcode'), 'street': vals.get('destination_street'), 'street2': vals.get('destination_street2'),
                 'street3': vals.get('destination_street3'), 'country_id': vals.get('destination_country_id'),
                 'location_url': vals.get('destination_location_map_url')})
            vals['destination_address_id'] = logistics_address.id

        vals['name'] = self.env['ir.sequence'].next_by_code('logistics.transport.order')
        return super(TransportOrder, self).create(vals)

    # ================================================================
    #               Onchange functions begins here
    # ================================================================

    @api.onchange('container_cleared_date', 'pullout_complete_date', 'waybill_date', 'pod_date', 'er_date', 'destination_arrival_date',
                  'cro_booking_date', 'empty_pickup_date', 'pol_date', 'shuttling_complete_date')
    def _update_state(self):
        for file in self:
            updates = {}
            warnings = {}

            if file.direction == 'import':
                if file.container_cleared_date:
                    updates['order_received'] = 'order_received'
                if file.pullout_complete_date and file.container_cleared_date:
                    updates['container_pulled_out'] = 'container_pulled_out'
                if file.pullout_complete_date and file.container_cleared_date and file.waybill_date:
                    updates['in_transit'] = 'in_transit'
                if file.pullout_complete_date and file.container_cleared_date and file.waybill_date and file.pod_date:
                    updates['received_pod'] = 'received_pod'
                if file.pullout_complete_date and file.container_cleared_date and file.waybill_date and file.pod_date and file.er_date:
                    updates['received_eir'] = 'received_eir'
                if file.pullout_complete_date and file.container_cleared_date and file.waybill_date and file.pod_date and file.er_date and file.destination_arrival_date:
                    updates['delivery_completed'] = 'delivery_completed'
            if file.direction == 'export':
                if file.cro_booking_date:
                    updates['order_received'] = 'order_received'
                if file.cro_booking_date and file.empty_pickup_date:
                    updates['container_picked_up'] = 'container_picked_up'
                if file.cro_booking_date and file.empty_pickup_date and file.waybill_date:
                    updates['in_transit'] = 'in_transit'
                if file.cro_booking_date and file.empty_pickup_date and file.waybill_date and file.pol_date:
                    updates['received_pol'] = 'received_pol'
                if file.cro_booking_date and file.empty_pickup_date and file.waybill_date and file.pol_date and file.shuttling_complete_date:
                    updates['port_shuttling'] = 'port_shuttling'
                if file.cro_booking_date and file.empty_pickup_date and file.waybill_date and file.pol_date and file.shuttling_complete_date and file.destination_arrival_date:
                    updates['delivery_completed'] = 'delivery_completed'

            for state, value in updates.items():
                file.update({'state': value})

            if file.state == 'delivery_completed':
                if not file.container_cleared_date:
                    warnings['container'] = "Container Cleared Date is required."
                if not file.waybill_date:
                    warnings['waybill'] = "Waybill Date is required."
                if not file.pod_date:
                    warnings['pod'] = "POD Date is required."

                warning_msgs = "\n".join(warnings.values()) if warnings else None

                if warning_msgs:
                    return {
                        'warning': {
                            'title': "Warning!",
                            'message': f"You cannot change these field values because the state is at Received EIR:\n{warning_msgs}"
                        }
                    }

    @api.onchange('direction')
    def _onchange_direction(self):
        values_to_update = {}
        if self.direction == 'import':
            values_to_update.update({'shuttling': False, 'make_empty_pickup': False, })
        elif self.direction == 'export':
            values_to_update.update({'make_pullout': False, 'make_empty_return': False, })
        self.update(values_to_update)

    @api.onchange('cargo_type', 'ltl_shipment_mode', 'ftl_shipment_mode')
    def _onchange_cargo_and_shipment_modes(self):
        if self.cargo_type == 'ltl':
            self.ftl_shipment_mode = False
        else:
            self.ltl_shipment_mode = False

        if self.ltl_shipment_mode:
            self.write({'shipment_mode': self.ltl_shipment_mode})

        if self.ftl_shipment_mode:
            self.write({'shipment_mode': self.ftl_shipment_mode})

    @api.onchange('make_pullout', 'make_empty_pickup', 'make_empty_pickup')
    def onchange_make_flags(self):
        fields_to_reset = []
        if not self.make_pullout:
            fields_to_reset.extend([
                'pullout_mode', 'pullout_vendor_id', 'pullout_fleet_id', 'pullout_fleet_name', 'pullout_driver_id', 'pullout_driver_name',
                'pullout_driver_mobile_number', 'pullout_trip_money_vendor_charges', 'pullout_status', 'pullout_schedule_date',
                'pullout_complete_date', 'pullout_port_id'
            ])
        if not self.make_empty_pickup:
            fields_to_reset.extend([
                'empty_pickup_mode', 'empty_pickup_vendor_id', 'empty_pickup_fleet_id', 'empty_pickup_fleet_name', 'empty_pickup_driver_id',
                'empty_pickup_driver_name', 'empty_pickup_driver_mobile_number', 'empty_pickup_trip_money_vendor_charges', 'empty_pickup_status',
                'empty_pickup_scheduled_date', 'empty_pickup_date'
            ])
        if not self.make_empty_pickup:
            fields_to_reset.extend([
                'er_mode', 'er_vendor_id', 'er_fleet_id', 'er_fleet_name', 'er_driver_id', 'er_driver_name', 'er_driver_mobile_number',
                'er_trip_money_vendor_charges', 'er_status', 'er_scheduled_date', 'er_date'
            ])
        self.update_fields(fields_to_reset)

    # Onchange functions for the transportation orders
    @api.onchange('transportation_mode')
    def _onchange_transportation_mode(self):
        values_to_update = {}
        if self.transportation_mode == 'internal':
            values_to_update.update({'driver_name': False, 'driver_mobile_number': False, 'vendor_id': False, 'fleet_type': False})
        elif self.transportation_mode == 'external':
            values_to_update.update(
                {'driver_id': False, 'driver_name': False, 'driver_mobile_number': False, 'fleet_name': False, 'fleet_type': False,
                 'fleet_id': False})
        self.update(values_to_update)

    @api.onchange('loading_address_id')
    def _onchange_loading_address_id(self):
        if self.loading_address_id:
            address_data = {
                'loading_address_name': self.loading_address_id.name, 'loading_address_code': self.loading_address_id.code,
                'loading_state_id': self.loading_address_id.state_id, 'loading_city_id': self.loading_address_id.city_id,
                'loading_zipcode': self.loading_address_id.zip_code, 'loading_street': self.loading_address_id.street,
                'loading_street2': self.loading_address_id.street2, 'loading_street3': self.loading_address_id.street3,
                'loading_location_map_url': self.loading_address_id.location_url,
            }
        else:
            address_data = {
                'loading_address_name': False, 'loading_address_code': False, 'loading_state_id': False, 'loading_city_id': False,
                'loading_zipcode': False, 'loading_street': False, 'loading_street2': False, 'loading_street3': False,
            }
        self.update(address_data)

    @api.onchange('destination_address_id')
    def _onchange_destination_address_id(self):
        values_to_update = {}
        if self.destination_address_id:
            values_to_update.update(
                {
                    'destination_address_name': self.destination_address_id.name, 'destination_address_code': self.destination_address_id.code,
                    'destination_state_id': self.destination_address_id.state_id.id, 'destination_city_id': self.destination_address_id.city_id.id,
                    'destination_zipcode': self.destination_address_id.zip_code, 'destination_street': self.destination_address_id.street,
                    'destination_street2': self.destination_address_id.street2, 'destination_street3': self.destination_address_id.street3,
                    'destination_location_map_url': self.destination_address_id.location_url,
                })
        else:
            values_to_update.update(
                {
                    'destination_address_name': False, 'destination_address_code': False, 'destination_state_id': False, 'destination_city_id': False,
                    'destination_zipcode': False, 'destination_street': False, 'destination_street2': False, 'destination_street3': False,
                })
        self.update(values_to_update)

    @api.onchange('loading_address_save_option')
    def _onchange_loading_address_save_option(self):
        self.loading_address_id = False if self.loading_address_save_option else self.loading_address_id

    @api.onchange('destination_address_save_option')
    def _onchange_destination_address_save_option(self):
        self.destination_address_id = False if self.destination_address_save_option else self.destination_address_id

    @api.onchange('container_number')
    def container_number_check_onchange(self):
        for rec in self:
            if rec.container_number:
                if len(rec.container_number) > 11 or not re.match('^[A-Z]{4}[0-9]{7,}$', rec.container_number.upper()):
                    raise ValidationError(f"Invalid Container Number Format: {rec.container_number.upper()}. It should be in the format ABCD1234567.")
                rec.container_number = rec.container_number.upper()

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        for rec in self:
            values_to_update = {}
            if rec.fleet_id:
                values_to_update.update({'fleet_name': rec.fleet_id.display_name, 'fleet_type': rec.fleet_id.category_id.name, })
                driver = rec.fleet_id.driver_id
                if driver:
                    values_to_update.update({'driver_id': driver.id, 'driver_name': driver.name, 'driver_mobile_number': driver.mobile, })
            rec.update(values_to_update)

    # Onchange functions of pullout
    @api.onchange('pullout_mode')
    def _onchange_pullout_mode(self):
        values_to_update = {}
        if self.pullout_mode in ['internal', 'external']:
            values_to_update.update(
                {'pullout_vendor_id': False, 'pullout_fleet_name': False, 'pullout_driver_name': False, 'pullout_driver_mobile_number': False})
        if self.pullout_mode == 'external':
            values_to_update.update({'pullout_fleet_id': False, 'pullout_driver_id': False})
        self.update(values_to_update)

    @api.onchange('pullout_fleet_id')
    def _onchange_pullout_fleet_id(self):
        values_to_update = {}
        if self.pullout_fleet_id:
            values_to_update.update({'pullout_fleet_name': self.pullout_fleet_id.name, 'pullout_driver_id': self.pullout_fleet_id.driver_id.id,
                                     'pullout_driver_name': self.pullout_fleet_id.driver_id.name,
                                     'pullout_driver_mobile_number': self.pullout_fleet_id.driver_id.mobile, })
        self.update(values_to_update)

    # Onchange functions of Empty Return
    @api.onchange('er_mode')
    def _onchange_er_mode(self):
        values_to_update = {'er_fleet_name': False, 'er_driver_name': False, 'er_vendor_id': False, 'er_driver_mobile_number': False}
        if self.er_mode == 'external':
            values_to_update.update({'er_fleet_id': False, 'er_driver_id': False})
        self.update(values_to_update)

    @api.onchange('er_fleet_id')
    def _onchange_er_fleet_id(self):
        values_to_update = {}
        if self.er_fleet_id:
            values_to_update.update({'er_fleet_name': self.er_fleet_id.name, })
            if self.er_fleet_id.driver_id:
                values_to_update.update({'er_driver_id': self.er_fleet_id.driver_id.id, 'er_driver_mobile_number': self.er_fleet_id.driver_id.mobile})
        self.update(values_to_update)

    # Onchange functions of Empty Pickup
    @api.onchange('make_empty_pickup')
    def _onchange_make_empty_pickup(self):
        if self.empty_pickup_status == 'finished':
            raise ValidationError(
                "In no uncertain terms, you must not switch the empty pickup status to false once the process has reached its conclusion.")

    @api.onchange('empty_pickup_mode')
    def _onchange_empty_pickup_mode(self):
        values_to_update = {}
        if self.empty_pickup_mode in ['internal', 'external']:
            values_to_update.update({'empty_pickup_vendor_id': False, 'empty_pickup_fleet_name': False, 'empty_pickup_driver_name': False,
                                     'empty_pickup_driver_mobile_number': False})
        if self.empty_pickup_mode == 'external':
            values_to_update.update({'empty_pickup_fleet_id': False, 'empty_pickup_driver_id': False})
        self.update(values_to_update)

    # Onchange functions of Breakdown
    @api.onchange('breakdown_mode')
    def _onchange_breakdown_mode(self):
        if self.breakdown_mode == 'external':
            self.update(
                {'breakdown_fleet_id': False, 'breakdown_fleet': False, 'breakdown_driver_id': False, 'breakdown_driver_mobile_number': False})
        elif self.breakdown_mode == 'internal':
            self.update(
                {'breakdown_vendor_id': False, 'breakdown_fleet': False, 'breakdown_driver': False, 'breakdown_driver_mobile_number': False})

    @api.onchange('breakdown_fleet_id')
    def _onchange_breakdown_fleet_id(self):
        values_to_update = {}
        if self.breakdown_fleet_id:
            values_to_update.update({'breakdown_fleet': self.breakdown_fleet_id.name, })
            if self.breakdown_fleet_id.driver_id:
                values_to_update.update({'breakdown_driver_id': self.breakdown_fleet_id.driver_id.id,
                                         'breakdown_driver_mobile_number': self.breakdown_fleet_id.driver_id.mobile, })
        self.update(values_to_update)

    # Onchange functions of Shuttling
    @api.onchange('shuttling_mode')
    def _onchange_shuttling_mode(self):
        values_to_update = {'shuttling_vendor_id': False, 'shuttling_fleet_name': False, 'shuttling_driver_name': False,
                            'shuttling_driver_mobile_number': False}
        if self.shuttling_mode == 'external':
            values_to_update.update({'shuttling_fleet_id': False, 'shuttling_driver_id': False})
        self.update(values_to_update)

    @api.onchange('shuttling_fleet_id')
    def _onchange_shuttling_fleet_id(self):
        values_to_update = {}
        if self.shuttling_fleet_id:
            values_to_update.update({'shuttling_fleet_name': self.shuttling_fleet_id.name, })
            if self.shuttling_fleet_id.driver_id:
                values_to_update.update(
                    {'shuttling_driver_id': self.shuttling_fleet_id.driver_id.id, 'shuttling_driver_name': self.shuttling_fleet_id.driver_id.name,
                     'shuttling_driver_mobile_number': self.shuttling_fleet_id.driver_id.mobile, })
        self.update(values_to_update)

    # ================================================================
    #               Normal functions begins here
    # ================================================================
    def update_fields(self, fields_to_reset):
        self.update({field: False for field in fields_to_reset})

    # Breakdown Buttons
    def make_breakdown(self):
        self.update({'breakdown_status': 'breakdown', 'breakdown_date': fields.Datetime.now()})

    def make_breakdown_inprogress(self):
        self.update({'breakdown_status': 'inprogress'})

    def make_breakdown_finished(self):
        self.update({'breakdown_status': 'finished'})

    # Pullout Buttons
    def pullout_trip(self):
        self.update({'pullout_status': 'inprogress'})

    def pullout_completed(self):
        self.update({'pullout_complete_date': fields.Date.today(), 'pullout_status': 'finished', 'state': 'container_pulled_out'})

    # Empty Pickup Buttons
    def ep_trip(self):
        self.update({'empty_pickup_status': 'inprogress'})

    def ep_completed(self):
        self.update({'empty_pickup_date': fields.Date.today(), 'empty_pickup_status': 'finished'})

    # Barcode generation for the waybill
    def generate_unique_barcode(self):
        if not self.barcode:
            barcode = str(uuid.uuid4())
            self.write({'barcode': barcode})
        return True

    # Print button function for the transport waybill
    def print_terminal_transport_waybill(self):
        if self.direction == 'import':
            if not (self.make_pullout and self.pullout_status == 'finished'):
                raise ValidationError("Finish the pullout process to process the waybill")
        self.update({'waybill_date': fields.Date.today(), 'state': 'in_transit'})
        self.generate_unique_barcode()
        return self.env.ref('ges_logistics.terminal_transport_waybill_report').report_action(self)


class LogisticsTransportCosts(models.Model):
    _name = 'logistics.transport.cost'
    _description = 'Transportation Cost'
    _rec_name = 'product_id'

    transport_id = fields.Many2one(comodel_name='logistics.transport.order', string="Transport ID", tracking=True, required=True)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", tracking=True, required=True)
    fleet_id = fields.Many2one(comodel_name='fleet.vehicle', string="Fleet", tracking=True)
    comments = fields.Char(string="Comments", tracking=True)
    attachment_name = fields.Char(string="Attachment Name", tracking=True)
    attachment = fields.Binary(string="Attachment", tracking=True)
