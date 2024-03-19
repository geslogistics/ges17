# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import re

_logger = logging.getLogger(__name__)


class CustomsOrder(models.Model):
    _name = "logistics.customs.order"
    _description = "Logistics Customs Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [('bl_number', 'unique (bl_number)', 'The BL Number must be unique, this one is already in the system.'),
                        ('awb_number', 'unique (awb_number)', 'The AWB Number must be unique, this one is already in the system.'),
                        ('lwb_number', 'unique (lwb_number)', 'The LWB Number must be unique, this one is already in the system.')]

    active = fields.Boolean(default=True, string='Active')
    source_ids = fields.Reference(selection=[('logistics.shipment.order', 'Shipment Order'), ('logistics.transport.order', 'Transport Order'),
                                             ('logistics.storage.order', 'Storage Order'), ('logistics.customs.order', 'Customs Order'),
                                             ('logistics.service.order', 'Service Order'), ('sale.order', 'Sale Order')], ondelete='restrict',
                                  string="Source")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency", related='company_id.currency_id')
    state = fields.Selection([('draft', 'Draft'), ('docs_received', 'Docs Received'), ('pre_clearance', 'Pre Clearance'),
                              ('clearance_fcd_issued', 'Clearance (Final CD Issued)'), ('clearance_completed', 'Clearance Completed'),
                              ('canceled', 'Canceled')], default='draft', string='State', tracking=True)
    name = fields.Char(string='Name', tracking=True, copy=False, default=lambda self: ('New'))

    # Customs Shipment Details
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', tracking=True)
    direction = fields.Selection(string="Direction", selection=[('import', 'Import'), ('export', 'Export')], tracking=True)
    ocean_shipment_mode = fields.Selection(
        [('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
         ('general_cargo_less_than_container_load_lcl', 'General Cargo > Less Than Container Load (LCL)'),
         ('general_cargo_break-bulk', 'General Cargo > Break-bulk'),
         ('general_cargo_neo-bulk', 'General Cargo > Neo-bulk'),
         ('roll-on/roll-off_roro_pure_car_carrier_pcc', 'Roll-on/roll-off (RoRo) > Pure Car Carrier (PCC)'),
         ('roll-on/roll-off_roro_pure_truck_and_car_carrier_pctc',
          'Roll-on/roll-off (RoRo) > Pure Truck and Car Carrier (PCTC)'),
         ('roll-on/roll-off_roro_cars_&_passenger_ropax', 'Roll-on/roll-off (RoRo) > Cars & Passenger (RoPax)'),
         ('roll-on/roll-off_roro_others', 'Roll-on/roll-off (RoRo) > Others'),
         ('loose_cargo_dry-bulk', 'Loose Cargo > Dry-bulk'),
         ('loose_cargo_liquid-bulk', 'Loose Cargo > Liquid-bulk'),
         ('loose_cargo_iso-tank', 'Loose Cargo > ISO-Tank'),
         ('loose_cargo_others', 'Loose Cargo > Others')], string="Shipment Type", tracking=True)
    air_shipment_mode = fields.Selection(
        [('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
         ('general_cargo_less_than_container_load_lcl', 'General Cargo > Less Than Container Load (LCL)'),
         ('general_cargo_break-bulk', 'General Cargo > Break-bulk'),
         ('special_cargo_live_animal', 'Special Cargo > Live Animal'),
         ('special_cargo_perishable_cargo', 'Special Cargo > Perishable Cargo'),
         ('special_cargo_mail_cargo', 'Special Cargo > Mail Cargo'),
         ('special_cargo_human_remains,_tissue,_and_organ_cargo',
          'Special Cargo > Human Remains, Tissue, and Organ Cargo'),
         ('special_cargo_dangerous_goods', 'Special Cargo > Dangerous Goods'),
         ('special_cargo_others', 'Special Cargo > Others')], string="Shipment Type", tracking=True)
    road_shipment_mode = fields.Selection(
        [('full_truck_load_ftl_flatbed_trailer', 'Full Truck Load (FTL) > Flatbed Trailer'),
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
    rail_shipment_mode = fields.Selection(
        [('full_truck_load_ftl_flatbed_trailer', 'Full Truck Load (FTL) > Flatbed Trailer'),
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
         ('others', 'Others')], string="Shipment Type", tracking=True)
    commodity_type = fields.Selection(string="Commodity Type", selection=[('general_cargo', 'General Cargo'), ('dangerous_goods', 'Dangerous Goods'),
                                                                          ('temperature_controlled', 'Temperature Controlled'),
                                                                          ('delicate_high_value', 'Delicate High Value'), ('roro', 'RoRo'),
                                                                          ('livestock', 'Livestock')], tracking=True)
    commercial_invoice = fields.Binary(string='Commercial Invoice')
    commercial_invoice_file_name = fields.Char(string='Commercial Invoice File Name', tracking=True)
    bl_number = fields.Char(string="BL Number", tracking=True, copy=False)
    awb_number = fields.Char(string="AWB Number", tracking=True, copy=False)
    lwb_number = fields.Char(string="LWB Number", tracking=True, copy=False)

    # Customer Details
    partner_id = fields.Many2one('res.partner', string="Customer", tracking=True)
    customer_reference = fields.Char(string="Customer Reference", tracking=True)
    # customer_reference_type_id = fields.Many2one(comodel_name='logistics.customer.reference.type', string="Customer Reference Type", tracking=True)
    billing_type = fields.Selection([('B/L Number', 'B/L Number'), ('Container Wise', 'Container Wise')], string="Billing Type", tracking=True)
    is_customer_agent = fields.Boolean(string="Is Agent?")

    # main carriage address
    main_carriage_country_id = fields.Many2one('logistics.freight.address.country', string="Country", ondelete='restrict',
                                               default=lambda self: self.env['logistics.freight.address.country'].search(
                                                   [('name', '=', 'Saudi Arabia')], limit=1))
    main_carriage_port_id = fields.Many2one('logistics.freight.port', string="Terminal at POL", ondelete='restrict')
    main_carriage_address_id = fields.Many2one('logistics.freight.address', string="From Address",
                                               domain="[('partner_id', '=', partner_id),('country_id', '=', main_carriage_country_id)]",
                                               ondelete='restrict')

    main_carriage_address_name = fields.Char(string='Port/Terminal Name')
    main_carriage_address_code = fields.Char(string='Port/Terminal Code')
    main_carriage_address_country_id = fields.Many2one('logistics.freight.address.country', string="Country", ondelete='restrict')
    main_carriage_address_state_id = fields.Many2one('logistics.freight.address.state', string="State",
                                                     domain="[('country_id', '=', main_carriage_address_country_id)]", ondelete='restrict')
    main_carriage_address_city_id = fields.Many2one('logistics.freight.address.city', string="City",
                                                    domain="[('country_id', '=', main_carriage_address_country_id)]", ondelete='restrict')
    main_carriage_address_zip_code = fields.Char(string="Zip Code")
    main_carriage_address_street = fields.Char(string="Street")
    main_carriage_address_street2 = fields.Char(string="Street 2")
    main_carriage_address_street3 = fields.Char(string="Street 3")

    # Shipment Details
    shipper_id = fields.Many2one("res.partner", string="Shipper", domain=[('shipper', '=', True)], tracking=True)
    consignee_id = fields.Many2one("res.partner", string="Consignee", domain=[('consignee', '=', True)], tracking=True)
    shipment_doc_received_date = fields.Date(string='Shipment Documents Received from Customer', tracking=True)
    broker_id = fields.Many2one(comodel_name='res.partner', string='Broker', domain=[('consignee', '=', True)], tracking=True)
    number_of_containers = fields.Integer("Number of Containers", compute="_compute_number_of_containers", tracking=True)
    number_of_packages = fields.Integer("Number of Packages", compute="_compute_number_of_packages", tracking=True)
    commodity_remarks = fields.Text("Commodity Remarks", tracking=True)
    ocean_status = fields.Selection(
        [('draft', 'Draft'), ('awaiting_shipment_docs', 'Awaiting Shipment Docs'), ('docs_received', 'Docs Received'),
         ('pending_vessel_arrival', 'Pending Vessel Arrival'), ('cargo_discharged_pending_bayan_print', 'Cargo Discharged - Pending Bayan Print'),
         ('pre_bayan_printed', 'Pre Bayan Printed'), ('shipment_cleared_pending_duty_payment', 'Shipment Cleared - Pending Duty Payment'),
         ('custom_duty_paid', 'Custom Duty Paid'), ('shipment_ready_for_pullout', 'Shipment Ready for PullOut'),
         ('transport_order_created_awaiting_port_shuttling', 'Transport Order Created - Awaiting Port Shuttling'),
         ('shipment_inside_port', 'Shipment Inside Port'), ('shipment_ready_to_load_in_vessel', 'Shipment Ready To Load in Vessel')], default="draft",
        tracking=True)

    # Shipment Information
    si_country_id = fields.Many2one('logistics.freight.address.country', string="Country", ondelete='restrict')
    si_port_id = fields.Many2one('logistics.freight.port', string="Port", ondelete='restrict')

    # Vessel , Airline and Truck Information
    vessel_name = fields.Char(string='Vessel Name', tracking=True)
    vessel_expected_arrival_date = fields.Date(string='Vessel Expected Arrival Date', tracking=True)
    vessel_arrival_date = fields.Date(string='Vessel Arrival Date', tracking=True)
    manifest_date = fields.Date(string='Manifest Date', tracking=True)
    discharge_date = fields.Date(string='Discharge Date', tracking=True)
    airline_id = fields.Many2one('logistics.freight.air.carriers', "Airline Carrier", tracking=True)
    flight_number = fields.Char("Flight Number", tracking=True)
    flight_departure_date = fields.Date("Flight Departure Date", tracking=True)
    flight_arrival_date = fields.Date("Flight Arrival Date", tracking=True)
    airline_operator_payment_date = fields.Date("Airline Operator Payment Date", tracking=True)
    internal_external = fields.Selection([('internal', 'Internal'), ('external', 'External')], tracking=True)
    fleet_id = fields.Many2one('fleet.vehicle', "Fleet", tracking=True)
    fleet_name = fields.Char("Fleet", tracking=True)
    driver_id = fields.Many2one('res.partner', "Driver", tracking=True)
    driver_name = fields.Char("Driver", tracking=True)
    driver_mobile_number = fields.Char("Driver Mobile Number", tracking=True)
    truck_departure_time = fields.Datetime("Truck Departure", tracking=True)
    truck_arrival_time = fields.Datetime("Truck Border Arrival Time", tracking=True)

    # Clearance Stage
    pre_customs_dec_no = fields.Char(string='Pre-Customs Declaration Number', tracking=True)
    pre_customs_dec_date = fields.Date(string='Pre-Customs Declaration Date', tracking=True)
    pre_customs_dec_attachment = fields.Binary(string='Pre-Customs Declaration Attachment')
    pre_customs_dec_attachment_filename = fields.Char(string='Pre-Customs Declaration Attachment', tracking=True)
    customs_duty_payment_notification_date = fields.Date(string='Custom Duty Payment Notification Date', tracking=True)
    customs_duty_payment_reference_number = fields.Char(string='Custom Duty Payment Reference Number', tracking=True)
    customs_duty_payment_amount = fields.Monetary(string='Custom Duty Payment Amount', currency_field='company_currency_id', tracking=True)
    customs_duty_payment_date = fields.Date(string='Custom Duty Payment Date', tracking=True)
    final_customs_declaration_date = fields.Date(string='Final Customs Declaration Date', tracking=True)
    final_customs_clearance_attachment = fields.Binary(string='Final Customs Declaration Attachment')
    final_customs_clearance_attachment_filename = fields.Char(string='Final Customs Declaration Attachment', tracking=True)
    broker_transportation_order_date = fields.Date(string='Broker Transportation Order Date', tracking=True)

    # Post Clearance Stage
    do_number = fields.Char(string='Delivery Order Number', tracking=True)
    do_collection_date = fields.Date(string='Delivery Order Collection Date', tracking=True)
    do_attachment = fields.Binary(string='Delivery Order Attachment')
    do_attachment_file_name = fields.Char(string='Delivery Order Attachment File Name', tracking=True)
    loading_card_date = fields.Date(string='Loading Card Date', tracking=True)
    pd_ce_payment_date = fields.Date(string='Port Dues and Customs Examination Payment Date', tracking=True)
    shipment_in_port_date = fields.Date(string='Shipment In Port Date', tracking=True)
    ok_to_load_date = fields.Date(string='OK To Load Date', tracking=True)
    inspection_date = fields.Date(string='Inspection Date', tracking=True)
    gate_pass_date = fields.Date(string='Gate Pass Date', tracking=True)

    # Demurrage and Detention Details
    demurrage_date = fields.Date(string='Demurrage Date', tracking=True)
    free_time_days = fields.Integer(string='Free Time Days', tracking=True, default=7)
    detention_date = fields.Date(string='Detention Date', tracking=True)

    # Additional Customs Information
    remarks = fields.Text(string="Remarks", tracking=True)
    clearance_time_taken = fields.Integer(string='Clearance Time Taken', tracking=True, compute='_compute_clearance_time_taken', store=True)
    clearance_delay_reason = fields.Text(string='Clearance Delay Reason', tracking=True)

    # One2Many Fields
    freight_package_ids = fields.One2many('shipment.package.line', 'customs_id')
    pr_ids = fields.One2many('payment.request', 'customs_id', string='Payment Requests')

    # Many2One fields
    so_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')

    @api.model
    def create(self, vals):
        # Determine direction and transport
        direction = 'IM' if vals.get('direction') == 'import' else 'EX'
        transport = vals.get('transport', '').upper()
        # Generate the sequence number
        sequence = self.env['ir.sequence'].next_by_code('logistics.customs.order')
        # Generate the name
        vals.setdefault('name', f'GES/CC/{direction}/{transport}/{sequence}')
        # Create the record
        record = super(CustomsOrder, self).create(vals)
        # Update ocean_status if not provided
        if not vals.get('ocean_status'):
            record._update_ocean_status_single()
        return record

    def write(self, vals):
        if 'direction' in vals:
            direction = 'IM' if vals['direction'] == 'import' else 'EX'
        else:
            direction = 'IM' if self.direction == 'import' else 'EX'

        if 'transport' in vals:
            transport = vals['transport'].upper()
        else:
            transport = self.transport.upper()

        # Update the name with the modified direction and transport
        # and retain the year and month parts from the existing name
        if self.name:
            parts = self.name.split('/')
            year_month = '/'.join(parts[-3:-1])
            vals['name'] = f'GES/CC/{direction}/{transport}/{year_month}/{parts[-1]}'

        res = super(CustomsOrder, self).write(vals)

        if 'ocean_status' not in vals:
            self._update_ocean_status_single()

        return res

    @api.onchange('shipment_doc_received_date', 'broker_id', 'pre_customs_dec_date', 'pre_customs_dec_no', 'final_customs_declaration_date')
    def _onchange_states(self):
        order_1 = self.shipment_doc_received_date and self.broker_id
        order_2 = self.pre_customs_dec_date and self.pre_customs_dec_no
        order_3 = self.final_customs_declaration_date
        if order_3:
            self.check_preclearance_related()
            self.check_fcd_related()
            self.state = 'clearance_fcd_issued'
        elif order_2:
            self.check_docreceived()
            self.check_preclearance_related()
            self.state = 'pre_clearance'
        elif not order_2 or not order_3:
            if self.shipment_doc_received_date and not self.broker_id:
                self.state = 'draft'
            elif not self.shipment_doc_received_date and self.broker_id:
                self.state = 'draft'
            elif not self.shipment_doc_received_date and not self.broker_id:
                self.state = 'draft'
            else:
                self.check_docreceived()
                self.state = 'docs_received'
        else:
            self._onchange_completion()

    @api.onchange('transport', 'direction', 'gate_pass_date', 'airline_operator_payment_date')
    def _onchange_completion(self):
        if (self.transport == 'ocean' and self.direction == 'import') and self.gate_pass_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'air' and self.direction == 'import') and self.airline_operator_payment_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'road' and self.direction == 'import') and self.gate_pass_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'rail' and self.direction == 'import') and self.gate_pass_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'ocean' and self.direction == 'export') and self.ok_to_load_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'air' and self.direction == 'export') and self.airline_operator_payment_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'road' and self.direction == 'export') and self.gate_pass_date:
            self.state = 'clearance_completed'
        elif (self.transport == 'rail' and self.direction == 'export') and self.gate_pass_date:
            self.state = 'clearance_completed'
        else:
            self._onchange_states()

    @api.depends('transport', 'si_country_id')
    @api.onchange('transport', 'si_country_id')
    def _onchange_transport_si_port_id(self):
        return {'domain': {'si_port_id': [(self.transport, '=', True), (
            'country_id', '=', self.si_country_id.id)]}}

    @api.depends('transport', 'main_carriage_country_id')
    @api.onchange('transport', 'main_carriage_country_id')
    def _onchange_transport_main_carriage_port_id(self):
        return {'domain': {'main_carriage_port_id': [(self.transport, '=', True), (
            'country_id', '=', self.main_carriage_country_id.id)]}}

    # reset main_carriage_port_id based on main_carriage_country_id
    @api.onchange('main_carriage_country_id', 'transport')
    def _onchange_main_carriage_country_id(self):
        self.main_carriage_port_id = False
        self.main_carriage_address_id = False
        if self.main_carriage_country_id:
            self.main_carriage_address_country_id = self.main_carriage_country_id.id
        else:
            self.main_carriage_address_country_id = False

    # update main carriage address
    @api.onchange('main_carriage_port_id', 'main_carriage_address_id', 'transport')
    def _onchange_main_carriage_port_id(self):
        if self.transport in ('ocean', 'air', 'rail'):
            if self.main_carriage_port_id:
                self.main_carriage_address_name = self.main_carriage_port_id.name
                self.main_carriage_address_code = self.main_carriage_port_id.code
                self.main_carriage_address_country_id = self.main_carriage_port_id.country_id.id
                self.main_carriage_address_state_id = self.main_carriage_port_id.state_id.id
                self.main_carriage_address_city_id = self.main_carriage_port_id.city_id.id
                self.main_carriage_address_zip_code = self.main_carriage_port_id.zip_code
                self.main_carriage_address_street = self.main_carriage_port_id.street
                self.main_carriage_address_street2 = self.main_carriage_port_id.street2
                self.main_carriage_address_street3 = self.main_carriage_port_id.street3
            else:
                self.main_carriage_address_name = False
                self.main_carriage_address_code = False
                self.main_carriage_address_country_id = False if self.main_carriage_country_id == False else self.main_carriage_country_id.id
                self.main_carriage_address_state_id = False
                self.main_carriage_address_city_id = False
                self.main_carriage_address_zip_code = False
                self.main_carriage_address_street = False
                self.main_carriage_address_street2 = False
                self.main_carriage_address_street3 = False
        if self.transport == 'road':
            if self.main_carriage_address_id:
                self.main_carriage_address_name = self.main_carriage_address_id.name
                self.main_carriage_address_code = self.main_carriage_address_id.code
                self.main_carriage_address_country_id = self.main_carriage_address_id.country_id.id
                self.main_carriage_address_state_id = self.main_carriage_address_id.state_id.id
                self.main_carriage_address_city_id = self.main_carriage_address_id.city_id.id
                self.main_carriage_address_zip_code = self.main_carriage_address_id.zip_code
                self.main_carriage_address_street = self.main_carriage_address_id.street
                self.main_carriage_address_street2 = self.main_carriage_address_id.street2
                self.main_carriage_address_street3 = self.main_carriage_address_id.street3
            else:
                self.main_carriage_address_name = False
                self.main_carriage_address_code = False
                self.main_carriage_address_country_id = False if self.main_carriage_country_id == False else self.main_carriage_country_id.id
                self.main_carriage_address_state_id = False
                self.main_carriage_address_city_id = False
                self.main_carriage_address_zip_code = False
                self.main_carriage_address_street = False
                self.main_carriage_address_street2 = False
                self.main_carriage_address_street3 = False

    @api.onchange('direction', 'partner_id')
    def _onchange_direction_partner_id(self):
        if self.direction == 'export':
            self.shipper_id = self.partner_id
            self.consignee_id = False
        elif self.direction == 'import':
            self.consignee_id = self.partner_id
            self.shipper_id = False
        else:
            self.shipper_id = self.consignee_id = False

    @api.onchange('transport')
    def _onchange_transport(self):
        self.clear_other_fields()

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.fleet_id:
            self.fleet_name = self.fleet_id.display_name
            driver = self.fleet_id.driver_id
            if driver:
                self.driver_id = driver.display_name
                self.driver_mobile_number = driver.mobile

    @api.depends('freight_package_ids.package_type')
    def _compute_number_of_containers(self):
        for order in self:
            order.number_of_containers = len(order.freight_package_ids.filtered(lambda x: x.package_type == 'container'))

    @api.depends('freight_package_ids.package_type')
    def _compute_number_of_packages(self):
        for order in self:
            order.number_of_packages = len(order.freight_package_ids.filtered(lambda x: x.package_type == 'item'))

    @api.depends('customs_duty_payment_date', 'discharge_date')
    def _compute_clearance_time_taken(self):
        for record in self:
            if record.customs_duty_payment_date and record.discharge_date:
                delta = record.customs_duty_payment_date - record.discharge_date
                record.clearance_time_taken = delta.days
            else:
                record.clearance_time_taken = 0

    @api.constrains('clearance_time_taken', 'clearance_delay_reason')
    def _check_clearance_delay_reason(self):
        for record in self:
            if record.clearance_time_taken >= 3:
                if not record.clearance_delay_reason or len(record.clearance_delay_reason.strip()) < 15:
                    raise ValidationError("Clearance Delay Reason must be at least 15 characters when Clearance Time Taken is 3 days or more.")

    def clear_other_fields(self):
        if self.transport == 'ocean':
            self.road_shipment_mode = False
            self.air_shipment_mode = False
            self.rail_shipment_mode = False
            self.awb_number = False
            self.lwb_number = False
            self.internal_external = False
            self.fleet_id = False
            self.fleet_name = False
            self.driver_id = False
            self.driver_name = False
            self.driver_mobile_number = False
            self.truck_departure_time = False
            self.truck_arrival_time = False
        elif self.transport == 'air':
            self.road_shipment_mode = False
            self.ocean_shipment_mode = False
            self.rail_shipment_mode = False
            self.bl_number = False
            self.lwb_number = False
            self.internal_external = False
            self.fleet_id = False
            self.fleet_name = False
            self.driver_id = False
            self.driver_name = False
            self.driver_mobile_number = False
            self.truck_departure_time = False
            self.truck_arrival_time = False
        elif self.transport == 'road':
            self.air_shipment_mode = False
            self.ocean_shipment_mode = False
            self.rail_shipment_mode = False
            self.bl_number = False
            self.awb_number = False
            self.airline_id = False
            self.flight_number = False
            self.flight_departure_date = False
            self.flight_arrival_date = False
            self.airline_operator_payment_date = False
            self.vessel_name = False
            self.vessel_expected_arrival_date = False
            self.vessel_arrival_date = False
            self.ocean_status = False
        elif self.transport == 'rail':
            self.road_shipment_mode = False
            self.ocean_shipment_mode = False
            self.air_shipment_mode = False
            self.bl_number = False
            self.awb_number = False
            self.airline_id = False
            self.flight_number = False
            self.flight_departure_date = False
            self.flight_arrival_date = False
            self.airline_operator_payment_date = False
            self.vessel_name = False
            self.vessel_expected_arrival_date = False
            self.vessel_arrival_date = False
            self.ocean_status = False
            self.internal_external = False
            self.fleet_id = False
            self.fleet_name = False
            self.driver_id = False
            self.driver_name = False
            self.driver_mobile_number = False
            self.truck_departure_time = False
            self.truck_arrival_time = False

    def check_fcd_related(self):
        if not self.pre_customs_dec_date:
            raise ValidationError("Enter the Pre Customs Declaration Date")
        elif not self.pre_customs_dec_no:
            raise ValidationError("Enter the Pre Customs Declaration Number")

    def check_preclearance_related(self):
        if not self.shipment_doc_received_date:
            raise ValidationError("Enter the Shipment Document Received from Customer to proceed")
        elif not self.broker_id:
            raise ValidationError("Enter the Broker ID to proceed")

    def check_docreceived(self):
        if not self.shipment_doc_received_date:
            raise ValidationError("Shipment Document Received date from the customer should be filled")
        elif not self.broker_id:
            raise ValidationError("Broker ID should be filled")

    def _update_ocean_status_single(self):
        """
        This private method updates the 'ocean_status' field of the CustomsOrder record(s)
        based on the values of various date fields and the 'direction' field.
        It checks conditions for both 'import' and 'export' directions and sets the
        appropriate 'ocean_status' value if the condition is met.
        """
        """Update ocean_status on current record only"""
        self.ensure_one()
        if self.direction == 'import':
            # Check and update ocean_status for 'import' direction
            if self.shipment_doc_received_date and self.ocean_status != 'docs_received':
                self.ocean_status = 'docs_received'
            elif self.vessel_expected_arrival_date and self.ocean_status != 'pending_vessel_arrival':
                self.ocean_status = 'pending_vessel_arrival'
            elif self.discharge_date and self.ocean_status != 'cargo_discharged_pending_bayan_print':
                self.ocean_status = 'cargo_discharged_pending_bayan_print'
            elif self.pre_customs_dec_date and self.ocean_status != 'pre_bayan_printed':
                self.ocean_status = 'pre_bayan_printed'
            elif self.customs_duty_payment_notification_date and self.ocean_status != 'shipment_cleared_pending_duty_payment':
                self.ocean_status = 'shipment_cleared_pending_duty_payment'
            elif self.customs_duty_payment_date and self.ocean_status != 'custom_duty_paid':
                self.ocean_status = 'custom_duty_paid'
            elif self.loading_card_date and self.ocean_status != 'shipment_ready_for_pullout':
                self.ocean_status = 'shipment_ready_for_pullout'
        elif self.direction == 'export':
            # Check and update ocean_status for 'export' direction
            if self.shipment_doc_received_date and self.ocean_status != 'docs_received':
                self.ocean_status = 'docs_received'
            elif self.vessel_expected_arrival_date and self.ocean_status != 'pending_vessel_arrival':
                self.ocean_status = 'pending_vessel_arrival'
            elif self.manifest_date and self.ocean_status != 'cargo_discharged_pending_bayan_print':
                self.ocean_status = 'cargo_discharged_pending_bayan_print'
            elif self.pre_customs_dec_date and self.ocean_status != 'pre_bayan_printed':
                self.ocean_status = 'pre_bayan_printed'
            elif self.broker_transportation_order_date and self.ocean_status != 'transport_order_created_awaiting_port_shuttling':
                self.ocean_status = 'transport_order_created_awaiting_port_shuttling'
            elif self.shipment_in_port_date and self.ocean_status != 'shipment_inside_port':
                self.ocean_status = 'shipment_inside_port'
            elif self.ok_to_load_date and self.ocean_status != 'shipment_ready_to_load_in_vessel':
                self.ocean_status = 'shipment_ready_to_load_in_vessel'

    def cancel_order(self):
        self.write({'state': 'canceled'})


class ShipmentPackageLine(models.Model):
    _name = 'shipment.package.line'
    _description = 'Freight Package Line'
    _rec_name = 'package'

    name = fields.Char(string='Container Number', required=True)
    customs_id = fields.Many2one('logistics.customs.order', string='Customs Order')
    package_type = fields.Selection([('item', 'Box / Cargo'), ('container', 'Container / Box')], string="Package Type")
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    package = fields.Many2one('freight.package', string='Size / Package', required=True)
    charges = fields.Monetary(related='package.charge', string='Charge')
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer'), ('flat_rock', 'Flat Rock'), ('open_top', 'Open Top'),
          ('other', 'Other')]), string="Type ")
    qty = fields.Float('Qty', required=True, default=1.0)
    harmonize = fields.Char('Harmonize')
    temperature = fields.Char('Temperature')
    humidity = fields.Char(string="Humidity")
    ventilation = fields.Char(string="Ventilation")
    vgm = fields.Char('VGM', help='Verified gross mass')
    carrier_seal = fields.Char('Carrier Seal')
    seal_number = fields.Char('Seal Number')
    reference = fields.Char('Reference')
    dangerous_goods = fields.Boolean('Dangerous Goods')
    class_number = fields.Char('Class Number')
    un_number = fields.Char('UN Number')
    Package_group = fields.Char('Packaging Group:')
    imdg_code = fields.Char('IMDG Code', help='International Maritime Dangerous Goods Code')
    flash_point = fields.Char('Flash Point')
    material_description = fields.Text('Material Description')
    freight_item_lines = fields.One2many('shipment.item', 'package_line_id')
    route_id = fields.Many2one('freight.route', 'Route')
    container_type = fields.Selection(
        [('GP', 'GP (General Purpose)'), ('HC', 'HC (High Cube)'),
         ('RF', 'RF (Reefer)'), ('FR', 'FR (Flat Rack)'),
         ('OT', 'OT (Open Top)'), ('GOH', 'GOH (Garment of Hanger)')], string="Type", default="GP")
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    net_weight = fields.Float(string="Net Weight (KG)")
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('name')
    def container_no_check_onchange(self):
        for rec in self:
            if rec.name:
                if len(rec.name) > 11:
                    raise ValidationError(
                        f"The container number exceeds the maximum length (11 characters): {rec.name}"
                    )
                if not re.match('^[A-Z]{4}[0-9]{7,}$', rec.name.upper()):
                    raise ValidationError(
                        f"You have Entered a Wrong Container Number or Format: {rec.name.upper()}\n"
                        "Format is ABCD1234567\n"
                        "First Four Characters Must be Alphabet and Last Seven Characters Must be Numeric"
                    )
                rec.name = rec.name.upper()

    @api.onchange('package')
    def _onchange_package_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.volume
                rec.gross_weight = rec.package.gross_weight
                rec.height = rec.package.height
                rec.length = rec.package.length
                rec.width = rec.package.width


class ShipmentItem(models.Model):
    _name = 'shipment.item'
    _description = 'Shipment Item Line'

    name = fields.Char(string='Description')
    package_line_id = fields.Many2one('shipment.package.line', 'Shipment ID')
    package = fields.Many2one('freight.package', 'Item')
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer')]), string="Operation")
    qty = fields.Float('Qty', default=1.0)
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('package')
    def _onchange_item_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.volume
                rec.gross_weight = rec.package.gross_weight
                rec.height = rec.package.height
                rec.length = rec.package.length
                rec.width = rec.package.width
                rec.name = rec.package.desc


class FreightPackage(models.Model):
    _name = 'freight.package'
    _description = 'Freight Package'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name / Size')
    container = fields.Boolean('Container/Box')
    item = fields.Boolean(string='Is Item')
    other = fields.Boolean('Other')
    active = fields.Boolean(default=True, string='Active')
    air = fields.Boolean(string='Air')
    ocean = fields.Boolean(string='Ocean')
    land = fields.Boolean(string='Land')
    desc = fields.Char(string="Description")
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')

    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', string='Currency')
    charge = fields.Monetary(string='Charges')
