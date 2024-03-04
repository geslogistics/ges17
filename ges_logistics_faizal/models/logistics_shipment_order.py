# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class ShipmentOrder(models.Model):
    _name = "logistics.shipment.order"
    _description = "Shipment Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    color = fields.Integer('Color')
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                              default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True,
                                  string='Currency')

    # status
    state = fields.Selection(
        [('new', 'Draft'), ('inprogress', 'In Progress'), ('confirmed', 'Confirmed'), ('intransit', 'In Transit'),
         ('delivered', 'Delivered'), ('cancel', 'Cancelled')], string='Status', copy=False, tracking=True,
        default='new')
    approval_state = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], string='Approval Status',
                                      copy=False, tracking=True, default='approved')

    # shipment main fields
    direction = fields.Selection(([('import', 'Import'), ('export', 'Export')]), string='Direction')
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]),
                                 string='Transport Via')
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
         ('loose_cargo_others', 'Loose Cargo > Others')], string="Shipment Type")
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
         ('special_cargo_others', 'Special Cargo > Others')], string="Shipment Type")
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
         ('others', 'Others'), ], string="Shipment Type")
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
         ('others', 'Others')], string="Shipment Type")

    # tracking
    tracking_number = fields.Char('Tracking Number')

    # One2many
    # sale_order_line_id = fields.One2many('sale.order.line', 'reference_document')

    # Customer fields
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict')
    customer_email = fields.Char(related='partner_id.email', string="Customer Email")
    customer_phone = fields.Char(related='partner_id.phone', string="Customer Phone")
    customer_mobile = fields.Char(related='partner_id.mobile', string="Customer Mobile")
    is_customer_agent = fields.Boolean(string="Is Agent?")

    # First Notify fields
    first_notify_id = fields.Many2one('res.partner', string='1st Notify', ondelete='restrict')
    first_notify_email = fields.Char(related='first_notify_id.email', string="1st Notify Email")
    first_notify_phone = fields.Char(related='first_notify_id.phone', string="1st Notify Phone")
    first_notify_mobile = fields.Char(related='first_notify_id.mobile', string="1st Notify Mobile")

    # Shipper
    shipper_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    shipper_email = fields.Char(related='shipper_id.email', string="Shipper Email")
    shipper_phone = fields.Char(related='shipper_id.phone', string="Shipper Phone")
    shipper_mobile = fields.Char(related='shipper_id.mobile', string="Shipper Mobile")

    # Consignee
    consignee_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    consignee_email = fields.Char(related='consignee_id.email', string="Consignee Email")
    consignee_phone = fields.Char(related='consignee_id.phone', string="Consignee Phone")
    consignee_mobile = fields.Char(related='consignee_id.mobile', string="Consignee Mobile")

    # Agent
    agent_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    agent_email = fields.Char(related='agent_id.email', string="Agent Email")
    agent_phone = fields.Char(related='agent_id.phone', string="Agent Phone")
    agent_mobile = fields.Char(related='agent_id.mobile', string="Agent Mobile")

    # origin main carriage address 
    origin_main_carriage_country_id = fields.Many2one('logistics.freight.address.country', string="Origin Country",
                                                      ondelete='restrict')
    origin_main_carriage_port_id = fields.Many2one('logistics.freight.port', string="Terminal at POL",
                                                   ondelete='restrict')
    origin_main_carriage_address_id = fields.Many2one('logistics.freight.address', string="From Address",
                                                      domain="[('partner_id', '=', partner_id),('country_id', '=', origin_main_carriage_country_id)]",
                                                      ondelete='restrict')
    origin_main_carriage_address_save_option = fields.Boolean(string="Save Address", store=False, default=False)

    origin_main_carriage_address_name = fields.Char(string='Port/Terminal Name')
    origin_main_carriage_address_code = fields.Char(string='Port/Terminal Code')
    origin_main_carriage_address_country_id = fields.Many2one('logistics.freight.address.country', string="Country",
                                                              ondelete='restrict')
    origin_main_carriage_address_state_id = fields.Many2one('logistics.freight.address.state', string="State",
                                                            domain="[('country_id', '=', origin_main_carriage_address_country_id)]",
                                                            ondelete='restrict')
    origin_main_carriage_address_city_id = fields.Many2one('logistics.freight.address.city', string="City",
                                                           domain="[('country_id', '=', origin_main_carriage_address_country_id)]",
                                                           ondelete='restrict')
    origin_main_carriage_address_zip_code = fields.Char(string="Zip Code")
    origin_main_carriage_address_street = fields.Char(string="Street")
    origin_main_carriage_address_street2 = fields.Char(string="Street 2")
    origin_main_carriage_address_street3 = fields.Char(string="Street 3")

    # origin pickup address
    pickup_option = fields.Boolean("Pick-up?")
    origin_pickup_country_id = fields.Many2one('logistics.freight.address.country', string="Origin Country",
                                               ondelete='restrict')
    origin_pickup_address_id = fields.Many2one('logistics.freight.address', string="Pick-Up Address",
                                               ondelete='restrict',
                                               domain="[('partner_id', '=', partner_id),('country_id', '=', origin_pickup_country_id)]")
    origin_pickup_address_save_option = fields.Boolean(string="Save Address", store=False, default=False)

    origin_pickup_address_name = fields.Char(string='Named Address Name')
    origin_pickup_address_code = fields.Char(string='Named Address Code')
    origin_pickup_address_country_id = fields.Many2one('logistics.freight.address.country', string="Country",
                                                       ondelete='restrict')
    origin_pickup_address_state_id = fields.Many2one('logistics.freight.address.state', string="State",
                                                     domain="[('country_id', '=', origin_pickup_address_country_id)]",
                                                     ondelete='restrict')
    origin_pickup_address_city_id = fields.Many2one('logistics.freight.address.city', string="City",
                                                    domain="[('country_id', '=', origin_pickup_address_country_id)]",
                                                    ondelete='restrict')
    origin_pickup_address_zip_code = fields.Char(string="Zip Code")
    origin_pickup_address_street = fields.Char(string="Street")
    origin_pickup_address_street2 = fields.Char(string="Street 2")
    origin_pickup_address_street3 = fields.Char(string="Street 3")

    # destination main carriage address
    destination_main_carriage_country_id = fields.Many2one('logistics.freight.address.country',
                                                           string="Destination Country", ondelete='restrict')
    destination_main_carriage_port_id = fields.Many2one('logistics.freight.port', string="Terminal at POD",
                                                        domain="[('country_id', '=', destination_main_carriage_country_id)]",
                                                        ondelete='restrict')
    destination_main_carriage_address_id = fields.Many2one('logistics.freight.address', string="To Address",
                                                           domain="[('partner_id', '=', partner_id),('country_id', '=', destination_main_carriage_country_id)]",
                                                           ondelete='restrict')
    destination_main_carriage_address_save_option = fields.Boolean(string="Save Address", store=False, default=False)

    destination_main_carriage_address_name = fields.Char(string='Port/Terminal Name')
    destination_main_carriage_address_code = fields.Char(string='Port/Terminal Code')
    destination_main_carriage_address_country_id = fields.Many2one('logistics.freight.address.country',
                                                                   string="Country", ondelete='restrict')
    destination_main_carriage_address_state_id = fields.Many2one('logistics.freight.address.state', string="State",
                                                                 domain="[('country_id', '=', destination_main_carriage_address_country_id)]",
                                                                 ondelete='restrict')
    destination_main_carriage_address_city_id = fields.Many2one('logistics.freight.address.city', string="City",
                                                                domain="[('country_id', '=', destination_main_carriage_address_country_id)]",
                                                                ondelete='restrict')
    destination_main_carriage_address_zip_code = fields.Char(string="Zip Code")
    destination_main_carriage_address_street = fields.Char(string="Street")
    destination_main_carriage_address_street2 = fields.Char(string="Street 2")
    destination_main_carriage_address_street3 = fields.Char(string="Street 3")

    # destination delivery address
    delivery_option = fields.Boolean("Delivery?")
    destination_delivery_country_id = fields.Many2one('logistics.freight.address.country', string="Destination Country",
                                                      ondelete='restrict')
    destination_delivery_address_id = fields.Many2one('logistics.freight.address', string="Delivery Address",
                                                      domain="[('partner_id', '=', partner_id),('country_id', '=', destination_delivery_country_id)]",
                                                      ondelete='restrict')
    destination_delivery_address_save_option = fields.Boolean(string="Save Address", store=False, default=False)

    destination_delivery_address_name = fields.Char(string='Named Address Name')
    destination_delivery_address_code = fields.Char(string='Named Address Code')
    destination_delivery_address_country_id = fields.Many2one('logistics.freight.address.country', string="Country",
                                                              ondelete='restrict')
    destination_delivery_address_state_id = fields.Many2one('logistics.freight.address.state', string="State",
                                                            domain="[('country_id', '=', destination_delivery_address_country_id)]",
                                                            ondelete='restrict')
    destination_delivery_address_city_id = fields.Many2one('logistics.freight.address.city', string="City",
                                                           domain="[('country_id', '=', destination_delivery_address_country_id)]",
                                                           ondelete='restrict')
    destination_delivery_address_zip_code = fields.Char(string="Zip Code")
    destination_delivery_address_street = fields.Char(string="Street")
    destination_delivery_address_street2 = fields.Char(string="Street 2")
    destination_delivery_address_street3 = fields.Char(string="Street 3")

    # incoterm
    incoterms_id = fields.Many2one('logistics.freight.incoterms', string='Incoterms', ondelete='restrict')

    # sale order fields
    so_ids = fields.Many2many('sale.order', string='Sales', copy=False, compute="_get_so_ids")
    so_ids_count = fields.Integer("Count of SOs", compute='_get_so_ids')
    so_ids_amount_untaxed = fields.Monetary("Sales Untaxed", digits=2, compute='_get_so_ids')
    so_ids_amount_tax = fields.Monetary("Sales Taxes", digits=2, compute='_get_so_ids')
    so_ids_amount_total = fields.Monetary("Sales Total", digits=2, compute='_get_so_ids')

    # Transportation Fields
    to_ids = fields.Many2many('logistics.transport.order', string='Transportation Orders', copy=False, compute="_get_to_ids")
    to_ids_count = fields.Integer("Count of Transportation Orders", compute='_get_to_ids')

    # quotations fields
    quotation_ids = fields.Many2many('sale.order', string='Quotations', copy=False, compute="_get_so_ids")
    quotation_ids_count = fields.Integer("Count of Quotations", compute='_get_so_ids')
    quotation_ids_amount_untaxed = fields.Monetary("Quotations Untaxed", digits=2, compute='_get_so_ids')
    quotation_ids_amount_tax = fields.Monetary("Quotations Taxes", digits=2, compute='_get_so_ids')
    quotation_ids_amount_total = fields.Monetary("Quotations Sales", digits=2, compute='_get_so_ids')

    # invoice fields
    invoice_ids = fields.Many2many('account.move', string='Invoices', copy=False, compute="_get_invoice_ids")
    invoice_ids_count = fields.Integer("Count of Invoices", compute='_get_invoice_ids')
    invoice_ids_amount_untaxed = fields.Monetary("Invoiced Untaxed", digits=2, compute='_get_invoice_ids')
    invoice_ids_amount_tax = fields.Monetary("Invoiced Taxes", digits=2, compute='_get_invoice_ids')
    invoice_ids_amount_total = fields.Monetary("Total Invoiced", digits=2, compute='_get_invoice_ids')

    invoice_ids_due = fields.Many2many('account.move', string='Due Invoices', copy=False, compute="_get_invoice_ids")
    invoice_ids_due_count = fields.Integer("Count of Due Invoices", compute='_get_invoice_ids')
    invoice_ids_due_amount_total = fields.Monetary("Total Dues", digits=2, compute='_get_invoice_ids')

    # services fields
    sol_ids = fields.Many2many('sale.order.line', string='Services', copy=False, compute="_get_sol_ids")
    sol_ids_count = fields.Integer("Count of Services", compute='_get_sol_ids')
    sol_ids_amount_untaxed = fields.Monetary("Services Untaxed", digits=2, compute='_get_sol_ids')
    sol_ids_amount_tax = fields.Monetary("Services Taxes", digits=2, compute='_get_sol_ids')
    sol_ids_amount_total = fields.Monetary("Services Total", digits=2, compute='_get_sol_ids')

    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            if values.get('transport') == 'air':
                air_pre = "GES/SH/AIR"
                values['name'] = air_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'ocean':
                ocean_pre = "GES/SH/OCEAN"
                values['name'] = ocean_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'road':
                road_pre = "GES/SH/ROAD"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'rail':
                road_pre = "GES/SH/RAIL"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
        if values.get('name', False) and not values.get('tracking_number', False):
            values['tracking_number'] = values.get('name', False)

        if not values.get('origin_main_carriage_address_id', False) and values.get(
                'origin_main_carriage_address_save_option', False) and values.get('transport', False) == 'road':
            newaddress_dict = {}
            if values.get('origin_main_carriage_address_name', False):
                newaddress_dict['name'] = values.get('origin_main_carriage_address_name', False)
            if values.get('origin_main_carriage_address_code', False):
                newaddress_dict['code'] = values.get('origin_main_carriage_address_code', False)
            if values.get('origin_main_carriage_address_country_id', False):
                newaddress_dict['country_id'] = values.get('origin_main_carriage_address_country_id', False)
            if values.get('origin_main_carriage_address_state_id', False):
                newaddress_dict['state_id'] = values.get('origin_main_carriage_address_state_id', False)
            if values.get('origin_main_carriage_address_city_id', False):
                newaddress_dict['city_id'] = values.get('origin_main_carriage_address_city_id', False)
            if values.get('origin_main_carriage_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('origin_main_carriage_address_zip_code', False)
            if values.get('origin_main_carriage_address_street', False):
                newaddress_dict['street'] = values.get('origin_main_carriage_address_street', False)
            if values.get('origin_main_carriage_address_street2', False):
                newaddress_dict['street2'] = values.get('origin_main_carriage_address_street2', False)
            if values.get('origin_main_carriage_address_street3', False):
                newaddress_dict['street3'] = values.get('origin_main_carriage_address_street3', False)
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['origin_main_carriage_address_id'] = newaddress.id

        if not values.get('destination_main_carriage_address_id', False) and values.get(
                'destination_main_carriage_address_save_option', False) and values.get('transport', False) == 'road':
            newaddress_dict = {}
            if values.get('destination_main_carriage_address_name', False):
                newaddress_dict['name'] = values.get('destination_main_carriage_address_name', False)
            if values.get('destination_main_carriage_address_code', False):
                newaddress_dict['code'] = values.get('destination_main_carriage_address_code', False)
            if values.get('destination_main_carriage_address_country_id', False):
                newaddress_dict['country_id'] = values.get('destination_main_carriage_address_country_id', False)
            if values.get('destination_main_carriage_address_state_id', False):
                newaddress_dict['state_id'] = values.get('destination_main_carriage_address_state_id', False)
            if values.get('destination_main_carriage_address_city_id', False):
                newaddress_dict['city_id'] = values.get('destination_main_carriage_address_city_id', False)
            if values.get('destination_main_carriage_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('destination_main_carriage_address_zip_code', False)
            if values.get('destination_main_carriage_address_street', False):
                newaddress_dict['street'] = values.get('destination_main_carriage_address_street', False)
            if values.get('destination_main_carriage_address_street2', False):
                newaddress_dict['street2'] = values.get('destination_main_carriage_address_street2', False)
            if values.get('destination_main_carriage_address_street3', False):
                newaddress_dict['street3'] = values.get('destination_main_carriage_address_street3', False)
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['destination_main_carriage_address_id'] = newaddress.id

        if not values.get('origin_pickup_address_id', False) and values.get('origin_pickup_address_save_option', False):
            newaddress_dict = {}
            if values.get('origin_pickup_address_name', False):
                newaddress_dict['name'] = values.get('origin_pickup_address_name', False)
            if values.get('origin_pickup_address_code', False):
                newaddress_dict['code'] = values.get('origin_pickup_address_code', False)
            if values.get('origin_pickup_address_country_id', False):
                newaddress_dict['country_id'] = values.get('origin_pickup_address_country_id', False)
            if values.get('origin_pickup_address_state_id', False):
                newaddress_dict['state_id'] = values.get('origin_pickup_address_state_id', False)
            if values.get('origin_pickup_address_city_id', False):
                newaddress_dict['city_id'] = values.get('origin_pickup_address_city_id', False)
            if values.get('origin_pickup_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('origin_pickup_address_zip_code', False)
            if values.get('origin_pickup_address_street', False):
                newaddress_dict['street'] = values.get('origin_pickup_address_street', False)
            if values.get('origin_pickup_address_street2', False):
                newaddress_dict['street2'] = values.get('origin_pickup_address_street2', False)
            if values.get('origin_pickup_address_street3', False):
                newaddress_dict['street3'] = values.get('origin_pickup_address_street3', False)
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['origin_pickup_address_id'] = newaddress.id

        if not values.get('destination_delivery_address_id', False) and values.get(
                'destination_delivery_address_save_option', False):
            newaddress_dict = {}
            if values.get('destination_delivery_address_name', False):
                newaddress_dict['name'] = values.get('destination_delivery_address_name', False)
            if values.get('destination_delivery_address_code', False):
                newaddress_dict['code'] = values.get('destination_delivery_address_code', False)
            if values.get('destination_delivery_address_country_id', False):
                newaddress_dict['country_id'] = values.get('destination_delivery_address_country_id', False)
            if values.get('destination_delivery_address_state_id', False):
                newaddress_dict['state_id'] = values.get('destination_delivery_address_state_id', False)
            if values.get('destination_delivery_address_city_id', False):
                newaddress_dict['city_id'] = values.get('destination_delivery_address_city_id', False)
            if values.get('destination_delivery_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('destination_delivery_address_zip_code', False)
            if values.get('destination_delivery_address_street', False):
                newaddress_dict['street'] = values.get('destination_delivery_address_street', False)
            if values.get('destination_delivery_address_street2', False):
                newaddress_dict['street2'] = values.get('destination_delivery_address_street2', False)
            if values.get('destination_delivery_address_street3', False):
                newaddress_dict['street3'] = values.get('destination_delivery_address_street3', False)
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['destination_delivery_address_id'] = newaddress.id

        result = super(ShipmentOrder, self).create(values)
        return result

    def write(self, values):
        if values.get('name', ('New')) == ('New'):
            if values.get('transport') == 'air':
                air_pre = "GES/SH/AIR"
                values['name'] = air_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'ocean':
                ocean_pre = "GES/SH/OCEAN"
                values['name'] = ocean_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _(
                    'New')
            elif values.get('transport') == 'road':
                road_pre = "GES/SH/ROAD"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'rail':
                road_pre = "GES/SH/RAIL"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
        if values.get('name', False) and not values.get('tracking_number', False):
            values['tracking_number'] = values.get('name', False)

        if not values.get('origin_main_carriage_address_id', False) and values.get(
                'origin_main_carriage_address_save_option', False) and values.get('transport', False) == 'road':
            newaddress_dict = {}
            if values.get('origin_main_carriage_address_name', False):
                newaddress_dict['name'] = values.get('origin_main_carriage_address_name', False)
            else:
                newaddress_dict['name'] = self.origin_main_carriage_address_name
            if values.get('origin_main_carriage_address_code', False):
                newaddress_dict['code'] = values.get('origin_main_carriage_address_code', False)
            else:
                newaddress_dict['code'] = self.origin_main_carriage_address_code
            if values.get('origin_main_carriage_address_country_id', False):
                newaddress_dict['country_id'] = values.get('origin_main_carriage_address_country_id', False)
            else:
                newaddress_dict['country_id'] = self.origin_main_carriage_address_country_id.id
            if values.get('origin_main_carriage_address_state_id', False):
                newaddress_dict['state_id'] = values.get('origin_main_carriage_address_state_id', False)
            else:
                newaddress_dict['state_id'] = self.origin_main_carriage_address_state_id.id
            if values.get('origin_main_carriage_address_city_id', False):
                newaddress_dict['city_id'] = values.get('origin_main_carriage_address_city_id', False)
            else:
                newaddress_dict['city_id'] = self.origin_main_carriage_address_city_id.id
            if values.get('origin_main_carriage_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('origin_main_carriage_address_zip_code', False)
            else:
                newaddress_dict['zip_code'] = self.origin_main_carriage_address_zip_code
            if values.get('origin_main_carriage_address_street', False):
                newaddress_dict['street'] = values.get('origin_main_carriage_address_street', False)
            else:
                newaddress_dict['street'] = self.origin_main_carriage_address_street
            if values.get('origin_main_carriage_address_street2', False):
                newaddress_dict['street2'] = values.get('origin_main_carriage_address_street2', False)
            else:
                newaddress_dict['street2'] = self.origin_main_carriage_address_street2
            if values.get('origin_main_carriage_address_street3', False):
                newaddress_dict['street3'] = values.get('origin_main_carriage_address_street3', False)
            else:
                newaddress_dict['street3'] = self.origin_main_carriage_address_street3
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)
            else:
                newaddress_dict['partner_id'] = self.partner_id.id

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['origin_main_carriage_address_id'] = newaddress.id

        if not values.get('destination_main_carriage_address_id', False) and values.get(
                'destination_main_carriage_address_save_option', False) and values.get('transport', False) == 'road':
            newaddress_dict = {}
            if values.get('destination_main_carriage_address_name', False):
                newaddress_dict['name'] = values.get('destination_main_carriage_address_name', False)
            else:
                newaddress_dict['name'] = self.destination_main_carriage_address_name
            if values.get('destination_main_carriage_address_code', False):
                newaddress_dict['code'] = values.get('destination_main_carriage_address_code', False)
            else:
                newaddress_dict['code'] = self.destination_main_carriage_address_code
            if values.get('destination_main_carriage_address_country_id', False):
                newaddress_dict['country_id'] = values.get('destination_main_carriage_address_country_id', False)
            else:
                newaddress_dict['country_id'] = self.destination_main_carriage_address_country_id.id
            if values.get('destination_main_carriage_address_state_id', False):
                newaddress_dict['state_id'] = values.get('destination_main_carriage_address_state_id', False)
            else:
                newaddress_dict['state_id'] = self.destination_main_carriage_address_state_id.id
            if values.get('destination_main_carriage_address_city_id', False):
                newaddress_dict['city_id'] = values.get('destination_main_carriage_address_city_id', False)
            else:
                newaddress_dict['city_id'] = self.destination_main_carriage_address_city_id.id
            if values.get('destination_main_carriage_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('destination_main_carriage_address_zip_code', False)
            else:
                newaddress_dict['zip_code'] = self.destination_main_carriage_address_zip_code
            if values.get('destination_main_carriage_address_street', False):
                newaddress_dict['street'] = values.get('destination_main_carriage_address_street', False)
            else:
                newaddress_dict['street'] = self.destination_main_carriage_address_street
            if values.get('destination_main_carriage_address_street2', False):
                newaddress_dict['street2'] = values.get('destination_main_carriage_address_street2', False)
            else:
                newaddress_dict['street2'] = self.destination_main_carriage_address_street2
            if values.get('destination_main_carriage_address_street3', False):
                newaddress_dict['street3'] = values.get('destination_main_carriage_address_street3', False)
            else:
                newaddress_dict['street3'] = self.destination_main_carriage_address_street3
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)
            else:
                newaddress_dict['partner_id'] = self.partner_id.id

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['destination_main_carriage_address_id'] = newaddress.id

        if not values.get('origin_pickup_address_id', False) and values.get('origin_pickup_address_save_option', False):
            newaddress_dict = {}
            if values.get('origin_pickup_address_name', False):
                newaddress_dict['name'] = values.get('origin_pickup_address_name', False)
            else:
                newaddress_dict['name'] = self.origin_pickup_address_name
            if values.get('origin_pickup_address_code', False):
                newaddress_dict['code'] = values.get('origin_pickup_address_code', False)
            else:
                newaddress_dict['code'] = self.origin_pickup_address_code
            if values.get('origin_pickup_address_country_id', False):
                newaddress_dict['country_id'] = values.get('origin_pickup_address_country_id', False)
            else:
                newaddress_dict['country_id'] = self.origin_pickup_address_country_id.id
            if values.get('origin_pickup_address_state_id', False):
                newaddress_dict['state_id'] = values.get('origin_pickup_address_state_id', False)
            else:
                newaddress_dict['state_id'] = self.origin_pickup_address_state_id.id
            if values.get('origin_pickup_address_city_id', False):
                newaddress_dict['city_id'] = values.get('origin_pickup_address_city_id', False)
            else:
                newaddress_dict['city_id'] = self.origin_pickup_address_city_id.id
            if values.get('origin_pickup_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('origin_pickup_address_zip_code', False)
            else:
                newaddress_dict['zip_code'] = self.origin_pickup_address_zip_code
            if values.get('origin_pickup_address_street', False):
                newaddress_dict['street'] = values.get('origin_pickup_address_street', False)
            else:
                newaddress_dict['street'] = self.origin_pickup_address_street
            if values.get('origin_pickup_address_street2', False):
                newaddress_dict['street2'] = values.get('origin_pickup_address_street2', False)
            else:
                newaddress_dict['street2'] = self.origin_pickup_address_street2
            if values.get('origin_pickup_address_street3', False):
                newaddress_dict['street3'] = values.get('origin_pickup_address_street3', False)
            else:
                newaddress_dict['street3'] = self.origin_pickup_address_street3
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)
            else:
                newaddress_dict['partner_id'] = self.partner_id.id

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['origin_pickup_address_id'] = newaddress.id

        if not values.get('destination_delivery_address_id', False) and values.get(
                'destination_delivery_address_save_option', False):
            newaddress_dict = {}
            if values.get('destination_delivery_address_name', False):
                newaddress_dict['name'] = values.get('destination_delivery_address_name', False)
            else:
                newaddress_dict['name'] = self.destination_delivery_address_name
            if values.get('destination_delivery_address_code', False):
                newaddress_dict['code'] = values.get('destination_delivery_address_code', False)
            else:
                newaddress_dict['code'] = self.destination_delivery_address_code
            if values.get('destination_delivery_address_country_id', False):
                newaddress_dict['country_id'] = values.get('destination_delivery_address_country_id', False)
            else:
                newaddress_dict['country_id'] = self.destination_delivery_address_country_id.id
            if values.get('destination_delivery_address_state_id', False):
                newaddress_dict['state_id'] = values.get('destination_delivery_address_state_id', False)
            else:
                newaddress_dict['state_id'] = self.destination_delivery_address_state_id.id
            if values.get('destination_delivery_address_city_id', False):
                newaddress_dict['city_id'] = values.get('destination_delivery_address_city_id', False)
            else:
                newaddress_dict['city_id'] = self.destination_delivery_address_city_id.id
            if values.get('destination_delivery_address_zip_code', False):
                newaddress_dict['zip_code'] = values.get('destination_delivery_address_zip_code', False)
            else:
                newaddress_dict['zip_code'] = self.destination_delivery_address_zip_code
            if values.get('destination_delivery_address_street', False):
                newaddress_dict['street'] = values.get('destination_delivery_address_street', False)
            else:
                newaddress_dict['street'] = self.destination_delivery_address_street
            if values.get('destination_delivery_address_street2', False):
                newaddress_dict['street2'] = values.get('destination_delivery_address_street2', False)
            else:
                newaddress_dict['street2'] = self.destination_delivery_address_street2
            if values.get('destination_delivery_address_street3', False):
                newaddress_dict['street3'] = values.get('destination_delivery_address_street3', False)
            else:
                newaddress_dict['street3'] = self.destination_delivery_address_street3
            if values.get('partner_id', False):
                newaddress_dict['partner_id'] = values.get('partner_id', False)
            else:
                newaddress_dict['partner_id'] = self.partner_id.id

            if newaddress_dict:
                newaddress = self.env['logistics.freight.address'].sudo().create(newaddress_dict)
                values['destination_delivery_address_id'] = newaddress.id

        result = super(ShipmentOrder, self).write(values)
        return result

    # change domain of origin_main_carriage_port_id based on transport
    @api.depends('transport', 'origin_main_carriage_country_id')
    @api.onchange('transport', 'origin_main_carriage_country_id')
    def _onchange_transport_origin_main_carriage_port_id(self):
        return {'domain': {'origin_main_carriage_port_id': [(self.transport, '=', True), (
            'country_id', '=', self.origin_main_carriage_country_id.id)]}}

    # change domain of destination_main_carriage_port_id based on transport
    @api.depends('transport', 'destination_main_carriage_country_id')
    @api.onchange('transport', 'destination_main_carriage_country_id')
    def _onchange_transport_destination_main_carriage_port_id(self):
        return {'domain': {'destination_main_carriage_port_id': [(self.transport, '=', True), (
            'country_id', '=', self.destination_main_carriage_country_id.id)]}}

    # update shipper and consignee based on direction & partner_id & is_customer_agent
    @api.onchange('partner_id', 'direction', 'is_customer_agent')
    def _onchange_customer_direction(self):
        if self.partner_id and self.direction:
            if self.direction == 'import':
                if self.is_customer_agent:
                    self.consignee_id = False
                    self.shipper_id = False
                    self.agent_id = self.partner_id.id
                else:
                    self.consignee_id = self.partner_id.id
                    self.shipper_id = False
                    self.agent_id = False
            else:
                if self.is_customer_agent:
                    self.consignee_id = False
                    self.shipper_id = False
                    self.agent_id = self.partner_id.id
                else:
                    self.consignee_id = False
                    self.shipper_id = self.partner_id.id
                    self.agent_id = False
        else:
            self.consignee_id = False
            self.shipper_id = False
            self.agent_id = False

    # reset origin_main_carriage_port_id based on origin_main_carriage_country_id
    @api.onchange('origin_main_carriage_country_id', 'transport')
    def _onchange_origin_main_carriage_country_id(self):
        self.origin_main_carriage_port_id = False
        self.origin_main_carriage_address_id = False
        self.origin_main_carriage_address_save_option = False
        if self.origin_main_carriage_country_id:
            self.origin_main_carriage_address_country_id = self.origin_main_carriage_country_id.id
        else:
            self.origin_main_carriage_address_country_id = False

    # update origin main carriage address
    @api.onchange('origin_main_carriage_port_id', 'origin_main_carriage_address_id', 'transport')
    def _onchange_origin_main_carriage_port_id(self):
        if self.transport in ('ocean', 'air', 'rail'):
            if self.origin_main_carriage_port_id:
                self.origin_main_carriage_address_name = self.origin_main_carriage_port_id.name
                self.origin_main_carriage_address_code = self.origin_main_carriage_port_id.code
                self.origin_main_carriage_address_country_id = self.origin_main_carriage_port_id.country_id.id
                self.origin_main_carriage_address_state_id = self.origin_main_carriage_port_id.state_id.id
                self.origin_main_carriage_address_city_id = self.origin_main_carriage_port_id.city_id.id
                self.origin_main_carriage_address_zip_code = self.origin_main_carriage_port_id.zip_code
                self.origin_main_carriage_address_street = self.origin_main_carriage_port_id.street
                self.origin_main_carriage_address_street2 = self.origin_main_carriage_port_id.street2
                self.origin_main_carriage_address_street3 = self.origin_main_carriage_port_id.street3
            else:
                self.origin_main_carriage_address_name = False
                self.origin_main_carriage_address_code = False
                self.origin_main_carriage_address_country_id = False if self.origin_main_carriage_country_id == False else self.origin_main_carriage_country_id.id
                self.origin_main_carriage_address_state_id = False
                self.origin_main_carriage_address_city_id = False
                self.origin_main_carriage_address_zip_code = False
                self.origin_main_carriage_address_street = False
                self.origin_main_carriage_address_street2 = False
                self.origin_main_carriage_address_street3 = False
        if self.transport == 'road':
            if self.origin_main_carriage_address_id:
                self.origin_main_carriage_address_name = self.origin_main_carriage_address_id.name
                self.origin_main_carriage_address_code = self.origin_main_carriage_address_id.code
                self.origin_main_carriage_address_country_id = self.origin_main_carriage_address_id.country_id.id
                self.origin_main_carriage_address_state_id = self.origin_main_carriage_address_id.state_id.id
                self.origin_main_carriage_address_city_id = self.origin_main_carriage_address_id.city_id.id
                self.origin_main_carriage_address_zip_code = self.origin_main_carriage_address_id.zip_code
                self.origin_main_carriage_address_street = self.origin_main_carriage_address_id.street
                self.origin_main_carriage_address_street2 = self.origin_main_carriage_address_id.street2
                self.origin_main_carriage_address_street3 = self.origin_main_carriage_address_id.street3
                self.origin_main_carriage_address_save_option = False
            else:
                self.origin_main_carriage_address_name = False
                self.origin_main_carriage_address_code = False
                self.origin_main_carriage_address_country_id = False if self.origin_main_carriage_country_id == False else self.origin_main_carriage_country_id.id
                self.origin_main_carriage_address_state_id = False
                self.origin_main_carriage_address_city_id = False
                self.origin_main_carriage_address_zip_code = False
                self.origin_main_carriage_address_street = False
                self.origin_main_carriage_address_street2 = False
                self.origin_main_carriage_address_street3 = False
                self.origin_main_carriage_address_save_option = False

    # reset destination_main_carriage_port_id based on destination_main_carriage_country_id
    @api.onchange('destination_main_carriage_country_id', 'transport')
    def _onchange_destination_main_carriage_country_id(self):
        self.destination_main_carriage_port_id = False
        self.destination_main_carriage_address_id = False
        self.destination_main_carriage_address_save_option = False
        if self.destination_main_carriage_country_id:
            self.destination_main_carriage_address_country_id = self.destination_main_carriage_country_id.id
        else:
            self.destination_main_carriage_address_country_id = False

    # update destination main carriage address
    @api.onchange('destination_main_carriage_port_id', 'destination_main_carriage_address_id', 'transport')
    def _onchange_destination_main_carriage_id(self):
        if self.transport in ('ocean', 'air', 'rail'):
            if self.destination_main_carriage_port_id:
                self.destination_main_carriage_address_name = self.destination_main_carriage_port_id.name
                self.destination_main_carriage_address_code = self.destination_main_carriage_port_id.code
                self.destination_main_carriage_address_country_id = self.destination_main_carriage_port_id.country_id.id
                self.destination_main_carriage_address_state_id = self.destination_main_carriage_port_id.state_id.id
                self.destination_main_carriage_address_city_id = self.destination_main_carriage_port_id.city_id.id
                self.destination_main_carriage_address_zip_code = self.destination_main_carriage_port_id.zip_code
                self.destination_main_carriage_address_street = self.destination_main_carriage_port_id.street
                self.destination_main_carriage_address_street2 = self.destination_main_carriage_port_id.street2
                self.destination_main_carriage_address_street3 = self.destination_main_carriage_port_id.street3
            else:
                self.destination_main_carriage_address_name = False
                self.destination_main_carriage_address_code = False
                self.destination_main_carriage_address_country_id = False if self.destination_main_carriage_country_id == False else self.destination_main_carriage_country_id.id
                self.destination_main_carriage_address_state_id = False
                self.destination_main_carriage_address_city_id = False
                self.destination_main_carriage_address_zip_code = False
                self.destination_main_carriage_address_street = False
                self.destination_main_carriage_address_street2 = False
                self.destination_main_carriage_address_street3 = False
        if self.transport == 'road':
            if self.destination_main_carriage_address_id:
                self.destination_main_carriage_address_name = self.destination_main_carriage_address_id.name
                self.destination_main_carriage_address_code = self.destination_main_carriage_address_id.code
                self.destination_main_carriage_address_country_id = self.destination_main_carriage_address_id.country_id.id
                self.destination_main_carriage_address_state_id = self.destination_main_carriage_address_id.state_id.id
                self.destination_main_carriage_address_city_id = self.destination_main_carriage_address_id.city_id.id
                self.destination_main_carriage_address_zip_code = self.destination_main_carriage_address_id.zip_code
                self.destination_main_carriage_address_street = self.destination_main_carriage_address_id.street
                self.destination_main_carriage_address_street2 = self.destination_main_carriage_address_id.street2
                self.destination_main_carriage_address_street3 = self.destination_main_carriage_address_id.street3
                self.destination_main_carriage_address_save_option = False
            else:
                self.destination_main_carriage_address_name = False
                self.destination_main_carriage_address_code = False
                self.destination_main_carriage_address_country_id = False if self.destination_main_carriage_country_id == False else self.destination_main_carriage_country_id.id
                self.destination_main_carriage_address_state_id = False
                self.destination_main_carriage_address_city_id = False
                self.destination_main_carriage_address_zip_code = False
                self.destination_main_carriage_address_street = False
                self.destination_main_carriage_address_street2 = False
                self.destination_main_carriage_address_street3 = False
                self.destination_main_carriage_address_save_option = False

    # reset origin_pickup_address_id based on origin_pickup_country_id
    @api.onchange('origin_pickup_country_id')
    def _onchange_origin_pickup_country_id(self):
        self.origin_pickup_address_id = False
        self.origin_pickup_address_name = False
        self.origin_pickup_address_code = False
        self.origin_pickup_address_country_id = False if self.origin_pickup_country_id == False else self.origin_pickup_country_id.id
        self.origin_pickup_address_state_id = False
        self.origin_pickup_address_city_id = False
        self.origin_pickup_address_zip_code = False
        self.origin_pickup_address_street = False
        self.origin_pickup_address_street2 = False
        self.origin_pickup_address_street3 = False
        self.origin_pickup_address_save_option = False

    # update origin pickup address
    @api.onchange('origin_pickup_address_id')
    def _onchange_origin_pickup_address_id(self):
        if self.origin_pickup_address_id:
            self.origin_pickup_address_name = self.origin_pickup_address_id.name
            self.origin_pickup_address_code = self.origin_pickup_address_id.code
            self.origin_pickup_address_country_id = self.origin_pickup_address_id.country_id.id
            self.origin_pickup_address_state_id = self.origin_pickup_address_id.state_id.id
            self.origin_pickup_address_city_id = self.origin_pickup_address_id.city_id.id
            self.origin_pickup_address_zip_code = self.origin_pickup_address_id.zip_code
            self.origin_pickup_address_street = self.origin_pickup_address_id.street
            self.origin_pickup_address_street2 = self.origin_pickup_address_id.street2
            self.origin_pickup_address_street3 = self.origin_pickup_address_id.street3
            self.origin_pickup_address_save_option = False
        else:
            # self.origin_pickup_address_name = False
            # self.origin_pickup_address_code = False
            self.origin_pickup_address_country_id = False if self.origin_pickup_country_id == False else self.origin_pickup_country_id.id
            # self.origin_pickup_address_state_id = False
            # self.origin_pickup_address_city_id = False
            # self.origin_pickup_address_zip_code = False
            # self.origin_pickup_address_street = False
            # self.origin_pickup_address_street2 = False
            # self.origin_pickup_address_street3 = False

    # reset destination_delivery_address_id based on destination_delivery_country_id
    @api.onchange('destination_delivery_country_id')
    def _onchange_destination_delivery_country_id(self):
        self.destination_delivery_address_id = False
        self.destination_delivery_address_name = False
        self.destination_delivery_address_code = False
        self.destination_delivery_address_country_id = False if self.destination_delivery_country_id == False else self.destination_delivery_country_id.id
        self.destination_delivery_address_state_id = False
        self.destination_delivery_address_city_id = False
        self.destination_delivery_address_zip_code = False
        self.destination_delivery_address_street = False
        self.destination_delivery_address_street2 = False
        self.destination_delivery_address_street3 = False
        self.destination_delivery_address_save_option = False

    # update delivery address
    @api.onchange('destination_delivery_address_id')
    def _onchange_destination_delivery_address_id(self):
        if self.destination_delivery_address_id:
            self.destination_delivery_address_name = self.destination_delivery_address_id.name
            self.destination_delivery_address_code = self.destination_delivery_address_id.code
            self.destination_delivery_address_country_id = self.destination_delivery_address_id.country_id.id
            self.destination_delivery_address_state_id = self.destination_delivery_address_id.state_id.id
            self.destination_delivery_address_city_id = self.destination_delivery_address_id.city_id.id
            self.destination_delivery_address_zip_code = self.destination_delivery_address_id.zip_code
            self.destination_delivery_address_street = self.destination_delivery_address_id.street
            self.destination_delivery_address_street2 = self.destination_delivery_address_id.street2
            self.destination_delivery_address_street3 = self.destination_delivery_address_id.street3
            self.destination_delivery_address_save_option = False
        else:
            # self.destination_delivery_address_name = False
            # self.destination_delivery_address_code = False
            self.destination_delivery_address_country_id = False if self.destination_delivery_country_id == False else self.destination_delivery_country_id.id
            # self.destination_delivery_address_state_id = False
            # self.destination_delivery_address_city_id = False
            # self.destination_delivery_address_zip_code = False
            # self.destination_delivery_address_street = False
            # self.destination_delivery_address_street2 = False
            # self.destination_delivery_address_street3 = False

    # update address_id on save_option
    @api.onchange('origin_main_carriage_address_save_option')
    def _onchange_origin_main_carriage_address_save_option(self):
        if self.origin_main_carriage_address_save_option:
            self.origin_main_carriage_address_id = False

    @api.onchange('destination_main_carriage_address_save_option')
    def _onchange_destination_main_carriage_address_save_option(self):
        if self.destination_main_carriage_address_save_option:
            self.destination_main_carriage_address_id = False

    @api.onchange('origin_pickup_address_save_option')
    def _onchange_origin_pickup_address_save_option(self):
        if self.origin_pickup_address_save_option:
            self.origin_pickup_address_id = False

    @api.onchange('destination_delivery_address_save_option')
    def _onchange_destination_delivery_address_save_option(self):
        if self.destination_delivery_address_save_option:
            self.destination_delivery_address_id = False

    def create_new_address(self):
        return {
            # 'name': self.order_id,
            'res_model': 'logistics.freight.address',
            'type': 'ir.actions.act_window',
            'context': {'default_partner_id': self.partner_id.id},
            'view_mode': 'form',
            'view_type': 'form',
            # 'view_id': self.env.ref("pickabite.payment_form_view").id,
            'target': 'new'
        }

    # sale order functions
    @api.depends('so_ids.order_line')
    def _get_so_ids(self):
        for record in self:
            sale_order_lines = record.env['sale.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))])
            sale_orders = sale_order_lines.order_id.filtered(
                lambda r: r.state in ('sale', 'done')) if sale_order_lines else False
            record.so_ids = sale_orders if sale_orders else False
            record.so_ids_count = len(sale_orders) if sale_orders else False
            record.so_ids_amount_untaxed = sum(line.amount_untaxed for line in sale_orders) if sale_orders else False
            record.so_ids_amount_tax = sum(line.amount_tax for line in sale_orders) if sale_orders else False
            record.so_ids_amount_total = sum(line.amount_total for line in sale_orders) if sale_orders else False

            quotations = sale_order_lines.order_id.filtered(
                lambda r: r.state in ('draft', 'sent')) if sale_order_lines else False
            record.quotation_ids = quotations if quotations else False
            record.quotation_ids_count = len(quotations) if quotations else False
            record.quotation_ids_amount_untaxed = sum(
                line.amount_untaxed for line in quotations) if quotations else False
            record.quotation_ids_amount_tax = sum(line.amount_tax for line in quotations) if quotations else False
            record.quotation_ids_amount_total = sum(line.amount_total for line in quotations) if quotations else False

    def action_view_so(self):
        self.ensure_one()
        result = {
            "name": "Sales Orders",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "domain": [('id', 'in', self.so_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_view_quotations(self):
        self.ensure_one()
        result = {
            "name": "Quotations",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "domain": [('id', 'in', self.quotation_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_view_transportation_orders(self):
        result = {
            "name": "TOs",
            "type": "ir.actions.act_window",
            "res_model": "logistics.transport.order",
            "domain": [('id', 'in', self.to_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    # invoice & due functions
    @api.depends('so_ids.order_line.invoice_lines')
    def _get_invoice_ids(self):
        for record in self:
            invoices = record.so_ids.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund'))
            record.invoice_ids = invoices if invoices else False
            record.invoice_ids_count = len(invoices) if invoices else False
            record.invoice_ids_amount_untaxed = sum(line.amount_untaxed_signed for line in invoices.filtered(
                lambda r: r.state == 'posted')) if invoices else False
            record.invoice_ids_amount_tax = sum(line.amount_tax_signed for line in
                                                invoices.filtered(lambda r: r.state == 'posted')) if invoices else False
            record.invoice_ids_amount_total = sum(line.amount_total_signed for line in invoices.filtered(
                lambda r: r.state == 'posted')) if invoices else False

            invoices_due = record.so_ids.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund') and r.amount_residual_signed > 0)
            record.invoice_ids_due = invoices_due if invoices_due else False
            record.invoice_ids_due_count = len(invoices_due) if invoices_due else False
            record.invoice_ids_due_amount_total = sum(line.amount_residual_signed for line in invoices_due.filtered(
                lambda r: r.state == 'posted')) if invoices_due else False

    def action_view_invoices(self):
        self.ensure_one()
        result = {
            "name": "Invoices",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', self.invoice_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_view_invoices_due(self):
        self.ensure_one()
        result = {
            "name": "Due Invoices",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', self.invoice_ids_due.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    # def create_transportation_orders(self):

    # sale order lines (services) functions
    @api.depends('so_ids.order_line')
    def _get_sol_ids(self):
        for record in self:
            sale_order_lines = record.env['sale.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))])
            record.sol_ids = sale_order_lines if sale_order_lines else False
            record.sol_ids_count = len(sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_untaxed = sum(
                line.price_subtotal for line in sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_tax = sum(line.price_tax for line in sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_total = sum(
                line.price_total for line in sale_order_lines) if sale_order_lines else False

    def _get_to_ids(self):
        for record in self:
            record.to_ids = self.env['logistics.transport.order'].sudo().search(
                [('source_ids', '=', ('%s,%s' % ('logistics.transport.order', record.id)))]).ids
            record.to_ids_count = len(record.to_ids)


class TransportOrderCreation(models.TransientModel):
    _name = 'logistics.transport.order.create'
    _description = 'Transport Order Creation'

    number_of_orders = fields.Integer(string="No. of orders to create")
    shipment_id = fields.Many2many('logistics.shipment.order', string="Shipment")

    def action_create_transport_orders(self):
        transportation_orders = self.env['logistics.transport.order']
        for i in range(self.number_of_orders):
            transport_order_vals = {'source_ids': '%s,%s' % ('logistics.transport.order', self.shipment_id.id),
                                    'partner_id': self.shipment_id.partner_id.id, 'direction': self.shipment_id.direction,
                                    'cargo_type': 'ltl' if 'ltl' in self.shipment_id.road_shipment_mode else 'ftl',
                                    'ltl_shipment_mode': self.shipment_id.road_shipment_mode if 'ltl' in self.shipment_id.road_shipment_mode else '',
                                    'ftl_shipment_mode': self.shipment_id.road_shipment_mode if 'ftl' in self.shipment_id.road_shipment_mode else '', }
            transportation_orders.create(transport_order_vals)
