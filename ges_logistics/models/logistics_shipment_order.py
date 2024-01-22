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
    user_id = fields.Many2one('res.users', string='Create User', index=True, tracking=True,
                              default=lambda self: self.env.user)
    sale_user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        related='partner_id.user_id',
        store=True)

    sale_team_id = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
        related='partner_id.team_id',
        store=True)
    
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True,
                                  string='Currency')

    # status
    state = fields.Selection(
        [('new', 'Draft'), ('quotation', 'Quotation Sent'), ('booked', 'Booked'), ('inprogress', 'In Progress'), ('confirmed', 'Confirmed'), ('intransit', 'In Transit'),
         ('delivered', 'Delivered'), ('closed', 'Closed'), ('cancel', 'Cancelled')], string='Status', copy=False, tracking=True,
        default='new')
    approval_state = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], string='Approval Status',
                                      copy=False, tracking=True, default='approved')

    # linkage / creation fields
    source_sol_id = fields.Many2one('sale.order.line', string="Source SOL", store=False)

    # shipment main fields
    direction = fields.Selection(([('import', 'Import'), ('export', 'Export')]), string='Direction', default="export")
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', default="ocean")
    shipment_type = fields.Selection([('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
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
         ('loose_cargo_others', 'Loose Cargo > Others'),
         ('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
         ('general_cargo_less_than_container_load_lcl', 'General Cargo > Less Than Container Load (LCL)'),
         ('general_cargo_break-bulk', 'General Cargo > Break-bulk'),
         ('special_cargo_live_animal', 'Special Cargo > Live Animal'),
         ('special_cargo_perishable_cargo', 'Special Cargo > Perishable Cargo'),
         ('special_cargo_mail_cargo', 'Special Cargo > Mail Cargo'),
         ('special_cargo_human_remains,_tissue,_and_organ_cargo',
          'Special Cargo > Human Remains, Tissue, and Organ Cargo'),
         ('special_cargo_others', 'Special Cargo > Others'),
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
         ('others', 'Others'),
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
         ('others', 'Others')], string="Shipment Type")
         
    ocean_shipment_type = fields.Selection(
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
         ('loose_cargo_others', 'Loose Cargo > Others')], string="Ocean Shipment Type", default="general_cargo_full_container_load_fcl")
    air_shipment_type = fields.Selection(
        [('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
         ('general_cargo_less_than_container_load_lcl', 'General Cargo > Less Than Container Load (LCL)'),
         ('general_cargo_break-bulk', 'General Cargo > Break-bulk'),
         ('special_cargo_live_animal', 'Special Cargo > Live Animal'),
         ('special_cargo_perishable_cargo', 'Special Cargo > Perishable Cargo'),
         ('special_cargo_mail_cargo', 'Special Cargo > Mail Cargo'),
         ('special_cargo_human_remains,_tissue,_and_organ_cargo',
          'Special Cargo > Human Remains, Tissue, and Organ Cargo'),
         ('special_cargo_others', 'Special Cargo > Others')], string="Air Shipment Type", default="general_cargo_full_container_load_fcl")
    road_shipment_type = fields.Selection(
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
         ('others', 'Others'), ], string="Road Shipment Type", default="full_truck_load_ftl_flatbed_trailer")
    rail_shipment_type = fields.Selection(
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
         ('others', 'Others')], string="Rail Shipment Type", default="full_truck_load_ftl_flatbed_trailer")

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

    # quotations fields
    quotation_ids = fields.Many2many('sale.order', string='Quotations', copy=False, compute="_get_so_ids")
    quotation_ids_count = fields.Integer("Count of Quotations", compute='_get_so_ids')
    quotation_ids_amount_untaxed = fields.Monetary("Quotations Untaxed", digits=2, compute='_get_so_ids')
    quotation_ids_amount_tax = fields.Monetary("Quotations Taxes", digits=2, compute='_get_so_ids')
    quotation_ids_amount_total = fields.Monetary("Quotations Sales", digits=2, compute='_get_so_ids')

    # quotations lines fields
    qol_ids = fields.Many2many('sale.order.line', string='Services', copy=False, compute="_get_qol_ids")
    qol_ids_count = fields.Integer("Count of Services Quoted", compute='_get_qol_ids')
    qol_ids_amount_untaxed = fields.Monetary("Services Quoted Untaxed", digits=2, compute='_get_qol_ids')
    qol_ids_amount_tax = fields.Monetary("Services Quoted Taxes", digits=2, compute='_get_qol_ids')
    qol_ids_amount_total = fields.Monetary("Services Quoted Total", digits=2, compute='_get_qol_ids')

    # sale order fields
    so_ids = fields.Many2many('sale.order', string='Sales', copy=False, compute="_get_so_ids")
    so_ids_count = fields.Integer("Count of SOs", compute='_get_so_ids')
    so_ids_amount_untaxed = fields.Monetary("Sales Untaxed", digits=2, compute='_get_so_ids')
    so_ids_amount_tax = fields.Monetary("Sales Taxes", digits=2, compute='_get_so_ids')
    so_ids_amount_total = fields.Monetary("Sales Total", digits=2, compute='_get_so_ids')

    # sale order lines fields
    sol_ids = fields.Many2many('sale.order.line', string='Services', copy=False, compute="_get_sol_ids")
    sol_ids_count = fields.Integer("Count of Services Rendered", compute='_get_sol_ids')
    sol_ids_amount_untaxed = fields.Monetary("Services Rendered Untaxed", digits=2, compute='_get_sol_ids')
    sol_ids_amount_tax = fields.Monetary("Services Rendered Taxes", digits=2, compute='_get_sol_ids')
    sol_ids_amount_total = fields.Monetary("Services Rendered Total", digits=2, compute='_get_sol_ids')

    # invoice fields
    invoice_ids = fields.Many2many('account.move', string='Invoices', copy=False, compute="_get_invoice_ids")
    invoice_ids_count = fields.Integer("Count of Invoices", compute='_get_invoice_ids')
    invoice_ids_amount_untaxed = fields.Monetary("Invoiced Untaxed", digits=2, compute='_get_invoice_ids')
    invoice_ids_amount_tax = fields.Monetary("Invoiced Taxes", digits=2, compute='_get_invoice_ids')
    invoice_ids_amount_total = fields.Monetary("Total Invoiced", digits=2, compute='_get_invoice_ids')

    invoice_ids_due = fields.Many2many('account.move', string='Due Invoices', copy=False, compute="_get_invoice_ids")
    invoice_ids_due_count = fields.Integer("Count of Due Invoices", compute='_get_invoice_ids')
    invoice_ids_due_amount_total = fields.Monetary("Total Dues", digits=2, compute='_get_invoice_ids')

    # invoices lines fields
    iol_ids = fields.Many2many('account.move.line', string='Services Invoiced', copy=False, compute="_get_iol_ids")
    iol_ids_count = fields.Integer("Count of Services Invoiced", compute='_get_iol_ids')
    iol_ids_amount_untaxed = fields.Monetary("Services Invoiced Untaxed", digits=2, compute='_get_iol_ids')
    iol_ids_amount_tax = fields.Monetary("Services Invoiced Taxes", digits=2, compute='_get_iol_ids')
    iol_ids_amount_total = fields.Monetary("Services Invoiced Total", digits=2, compute='_get_iol_ids')



    # Vendor RFQ fields
    rfq_ids = fields.Many2many('purchase.order', string='RFQs', copy=False, compute="_get_po_ids")
    rfq_ids_count = fields.Integer("Count of RFQs", compute='_get_po_ids')
    rfq_ids_amount_untaxed = fields.Monetary("RFQs Untaxed", digits=2, compute='_get_po_ids')
    rfq_ids_amount_tax = fields.Monetary("RFQs Taxes", digits=2, compute='_get_po_ids')
    rfq_ids_amount_total = fields.Monetary("RFQs Sales", digits=2, compute='_get_po_ids')

    # RFQs lines fields
    rfqol_ids = fields.Many2many('purchase.order.line', string='Services', copy=False, compute="_get_rfqol_ids")
    rfqol_ids_count = fields.Integer("Count of Services Requested", compute='_get_rfqol_ids')
    rfqol_ids_amount_untaxed = fields.Monetary("Services Requested Untaxed", digits=2, compute='_get_rfqol_ids')
    rfqol_ids_amount_tax = fields.Monetary("Services Requested Taxes", digits=2, compute='_get_rfqol_ids')
    rfqol_ids_amount_total = fields.Monetary("Services Requested Total", digits=2, compute='_get_rfqol_ids')

    # vendor purchase order fields
    po_ids = fields.Many2many('purchase.order', string='Purchases', copy=False, compute="_get_po_ids")
    po_ids_count = fields.Integer("Count of POs", compute='_get_po_ids')
    po_ids_amount_untaxed = fields.Monetary("Purchases Untaxed", digits=2, compute='_get_po_ids')
    po_ids_amount_tax = fields.Monetary("Purchases Taxes", digits=2, compute='_get_po_ids')
    po_ids_amount_total = fields.Monetary("Purchases Total", digits=2, compute='_get_po_ids')

    # services received fields
    pol_ids = fields.Many2many('purchase.order.line', string='Purchases', copy=False, compute="_get_pol_ids")
    pol_ids_count = fields.Integer("Count of Services Received", compute='_get_pol_ids')
    pol_ids_amount_untaxed = fields.Monetary("Services Received Untaxed", digits=2, compute='_get_pol_ids')
    pol_ids_amount_tax = fields.Monetary("Services Received Taxes", digits=2, compute='_get_pol_ids')
    pol_ids_amount_total = fields.Monetary("Services Received Total", digits=2, compute='_get_pol_ids')

    # vendor bill fields
    bill_ids = fields.Many2many('account.move', string='Bills', copy=False, compute="_get_bill_ids")
    bill_ids_count = fields.Integer("Count of Bills", compute='_get_bill_ids')
    bill_ids_amount_untaxed = fields.Monetary("Billed Untaxed", digits=2, compute='_get_bill_ids')
    bill_ids_amount_tax = fields.Monetary("Billed Taxes", digits=2, compute='_get_bill_ids')
    bill_ids_amount_total = fields.Monetary("Total Billed", digits=2, compute='_get_bill_ids')

    bill_ids_due = fields.Many2many('account.move', string='Due Bills', copy=False, compute="_get_bill_ids")
    bill_ids_due_count = fields.Integer("Count of Due Bills", compute='_get_bill_ids')
    bill_ids_due_amount_total = fields.Monetary("Total Dues", digits=2, compute='_get_bill_ids')

    # bills lines fields
    bol_ids = fields.Many2many('account.move.line', string='Services Billed', copy=False, compute="_get_bol_ids")
    bol_ids_count = fields.Integer("Count of Services Billed", compute='_get_bol_ids')
    bol_ids_amount_untaxed = fields.Monetary("Services Billed Untaxed", digits=2, compute='_get_bol_ids')
    bol_ids_amount_tax = fields.Monetary("Services Billed Taxes", digits=2, compute='_get_bol_ids')
    bol_ids_amount_total = fields.Monetary("Services Billed Total", digits=2, compute='_get_bol_ids')

    

    # general information fields
    bl_number = fields.Char(string="B/L")
    
    special_instructions = fields.Text(string="Special Instruction")
    contact_place_of_receipt = fields.Selection([('Shipper', 'Shipper'), ('Consignee', 'Consignee')],
                                                string="Place of Receipt", default="Consignee")
    contact_place_of_delivery = fields.Selection([('Shipper', 'Shipper'), ('Consignee', 'Consignee')],
                                                 string="Place of Delivery", default="Consignee")
    move_type_id = fields.Many2one('logistics.freight.move.type', 'Move Type')
    move_type_code = fields.Char(related="move_type_id.code")
    incoterms_id = fields.Many2one('logistics.freight.incoterms', string='Incoterms', ondelete='restrict')
    incoterms_code = fields.Char(related="incoterms_id.code")
    delivery_terms = fields.Selection([('pp', 'Prepaid (PP)'), ('cc', 'Collect (CC)'),('cp','Prepaid/Collect (CP)')], string="Delivery Terms")
    delivery_terms_code = fields.Char("Delivery Terms Code", compute="_get_delivery_terms_code")

    is_dangerous = fields.Boolean(string="Dangerous Goods")
    notes = fields.Text('Notes')

    # packages

    freight_packages = fields.One2many('logistics.shipment.package.line', 'shipment_id')

    ## Total Net, Gross and Volume
    package_total_gross = fields.Float(compute="_compute_total_gross_net_volume")
    package_total_net = fields.Float(compute="_compute_total_gross_net_volume")
    package_total_volume = fields.Float(compute="_compute_total_gross_net_volume")

    ############# Functions

    ### delete conditions
    def unlink(self):
        for record in self:
            currentrec = str('%s,%s' % (record._name, record.id))
            
            so_ids = record.env['sale.order.line'].search([('reference_document', '=', currentrec)])
            po_ids = record.env['purchase.order.line'].search([('reference_document', '=', currentrec)])
            invoice_ids = record.env['account.move.line'].search([('reference_document', '=', currentrec)]).filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
            bill_ids = record.env['account.move.line'].search([('reference_document', '=', currentrec)]).filtered(lambda r: r.move_type in ('in_invoice', 'in_refund'))

            if so_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Sale Order " + str([so_ids.order_id[0].name])))
            if po_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Purchase Order " + str([po_ids.order_id[0].name])))
            if invoice_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Customer Invoice " + str([invoice_ids.move_id[0].name])))
            if bill_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Vendor Bill " + str([bill_ids.move_id[0].name])))
    
        return super(ShipmentOrder, self).unlink()

    @api.onchange('ocean_shipment_type','air_shipment_type','road_shipment_type','rail_shipment_type')
    def _onchange_shipment_type(self):
        if self.transport == 'ocean':
            self.shipment_type = self.ocean_shipment_type
        elif self.transport == 'air':
            self.shipment_type = self.air_shipment_type
        elif self.transport == 'road':
            self.shipment_type = self.road_shipment_type
        elif self.transport == 'rail':
            self.shipment_type = self.rail_shipment_type

    @api.onchange('delivery_terms')
    @api.depends('delivery_terms')
    def _get_delivery_terms_code(self):
        if self.delivery_terms == 'pp':
            self.delivery_terms_code = 'PP'
        elif self.delivery_terms == 'cc':
            self.delivery_terms_code = 'CC'
        elif self.delivery_terms == 'cp':
            self.delivery_terms_code = 'CP'
        else:
            self.delivery_terms_code = False

    

    @api.depends('freight_packages')
    def _compute_total_gross_net_volume(self):
        for rec in self:
            net = 0.0
            gross = 0.0
            volume = 0.0
            if rec.freight_packages:
                for data in rec.freight_packages:
                    net = net + data.net_weight
                    gross = gross + data.gross_weight
                    volume = volume + data.volume
            rec.package_total_volume = volume
            rec.package_total_net = net
            rec.package_total_gross = gross

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            if order.partner_id and not (order._origin.id and order.sale_user_id):
                # Recompute the salesman on partner change
                #   * if partner is set (is required anyway, so it will be set sooner or later)
                #   * if the order is not saved or has no salesman already
                order.sale_user_id = (
                    order.partner_id.user_id
                    or order.partner_id.commercial_partner_id.user_id
                    or (self.user_has_groups('sales_team.group_sale_salesman') and self.env.user)
                )

    @api.depends('partner_id', 'sale_user_id')
    def _compute_team_id(self):
        cached_teams = {}
        for order in self:
            default_team_id = self.env.context.get('default_team_id', False) or order.sale_team_id.id or order.partner_id.team_id.id
            user_id = order.sale_user_id.id
            company_id = order.company_id.id
            key = (default_team_id, user_id, company_id)
            if key not in cached_teams:
                cached_teams[key] = self.env['crm.team'].with_context(
                    default_team_id=default_team_id
                )._get_default_team_id(
                    user_id=user_id, domain=[('company_id', 'in', [company_id, False])])
            order.sale_team_id = cached_teams[key]


    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            if values.get('transport') == 'air':
                air_pre = "GES/SHO"
                values['name'] = air_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'ocean':
                ocean_pre = "GES/SHO"
                values['name'] = ocean_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'road':
                road_pre = "GES/SHO"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'rail':
                road_pre = "GES/SHO"
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
        
        if values.get('source_sol_id', False):
            self.env['sale.order.line'].search([('id','=',values.get('source_sol_id', False))]).write({'reference_document':('%s,%s' % ('logistics.shipment.order',result.id))})
        
        return result

    def write(self, values):
        if values.get('name', ('New')) == ('New'):
            if values.get('transport') == 'air':
                air_pre = "GES/SHO"
                values['name'] = air_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'ocean':
                ocean_pre = "GES/SHO"
                values['name'] = ocean_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _(
                    'New')
            elif values.get('transport') == 'road':
                road_pre = "GES/SHO"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('logistics.shipment.order') or _('New')
            elif values.get('transport') == 'rail':
                road_pre = "GES/SHO"
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

    # quotations lines (services quoted) functions
    @api.depends('quotation_ids.order_line')
    def _get_qol_ids(self):
        for record in self:
            quotation_lines = record.env['sale.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.order_id.state in ('draft', 'sent'))
            record.qol_ids = quotation_lines if quotation_lines else False
            record.qol_ids_count = len(quotation_lines) if quotation_lines else False
            record.qol_ids_amount_untaxed = sum(
                line.price_subtotal for line in quotation_lines) if quotation_lines else False
            record.qol_ids_amount_tax = sum(line.price_tax for line in quotation_lines) if quotation_lines else False
            record.qol_ids_amount_total = sum(
                line.price_total for line in quotation_lines) if quotation_lines else False

    # sale order lines (services rendered) functions
    @api.depends('so_ids.order_line')
    def _get_sol_ids(self):
        for record in self:
            sale_order_lines = record.env['sale.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.order_id.state in ('sale', 'done'))
            record.sol_ids = sale_order_lines if sale_order_lines else False
            record.sol_ids_count = len(sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_untaxed = sum(
                line.price_subtotal for line in sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_tax = sum(line.price_tax for line in sale_order_lines) if sale_order_lines else False
            record.sol_ids_amount_total = sum(
                line.price_total for line in sale_order_lines) if sale_order_lines else False

    # Invoice lines (services invoiced) functions
    @api.depends('invoice_ids.invoice_line_ids')
    def _get_iol_ids(self):
        for record in self:
            invoice_lines = record.env['account.move.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.move_id.move_type in ('out_invoice', 'out_refund') and r.move_id.state == 'posted')
            record.iol_ids = invoice_lines if invoice_lines else False
            record.iol_ids_count = len(invoice_lines) if invoice_lines else False
            record.iol_ids_amount_untaxed = sum(
                line.price_subtotal for line in invoice_lines) if invoice_lines else False
            record.iol_ids_amount_tax = sum(line.tax_base_amount for line in invoice_lines) if invoice_lines else False
            record.iol_ids_amount_total = sum(
                line.price_total for line in invoice_lines) if invoice_lines else False




    # purchase order functions
    @api.depends('po_ids.order_line')
    def _get_po_ids(self):
        for record in self:
            purchase_order_lines = record.env['purchase.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))])
            purchase_orders = purchase_order_lines.order_id.filtered(
                lambda r: r.state in ('purchase', 'done')) if purchase_order_lines else False
            record.po_ids = purchase_orders if purchase_orders else False
            record.po_ids_count = len(purchase_orders) if purchase_orders else False
            record.po_ids_amount_untaxed = sum(line.amount_untaxed for line in purchase_orders) if purchase_orders else False
            record.po_ids_amount_tax = sum(line.amount_tax for line in purchase_orders) if purchase_orders else False
            record.po_ids_amount_total = sum(line.amount_total for line in purchase_orders) if purchase_orders else False

            rfqs = purchase_order_lines.order_id.filtered(
                lambda r: r.state in ('draft', 'sent','to approve')) if purchase_order_lines else False
            record.rfq_ids = rfqs if rfqs else False
            record.rfq_ids_count = len(rfqs) if rfqs else False
            record.rfq_ids_amount_untaxed = sum(
                line.amount_untaxed for line in rfqs) if rfqs else False
            record.rfq_ids_amount_tax = sum(line.amount_tax for line in rfqs) if rfqs else False
            record.rfq_ids_amount_total = sum(line.amount_total for line in rfqs) if rfqs else False

    def action_view_po(self):
        self.ensure_one()
        result = {
            "name": "Purchase Orders",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [('id', 'in', self.po_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_view_rfqs(self):
        self.ensure_one()
        result = {
            "name": "RFQs",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [('id', 'in', self.rfq_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    # bill & due functions
    @api.depends('po_ids.order_line.invoice_lines')
    def _get_bill_ids(self):
        for record in self:
            bills = record.po_ids.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('in_invoice', 'in_refund'))
            record.bill_ids = bills if bills else False
            record.bill_ids_count = len(bills) if bills else False
            record.bill_ids_amount_untaxed = sum(line.amount_untaxed_signed for line in bills.filtered(
                lambda r: r.state == 'posted')) if bills else False
            record.bill_ids_amount_tax = sum(line.amount_tax_signed for line in
                                                bills.filtered(lambda r: r.state == 'posted')) if bills else False
            record.bill_ids_amount_total = sum(line.amount_total_signed for line in bills.filtered(
                lambda r: r.state == 'posted')) if bills else False

            bills_due = record.po_ids.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('in_invoice', 'in_refund') and r.amount_residual_signed < 0)
            record.bill_ids_due = bills_due if bills_due else False
            record.bill_ids_due_count = len(bills_due) if bills_due else False
            record.bill_ids_due_amount_total = sum(line.amount_residual_signed for line in bills_due.filtered(
                lambda r: r.state == 'posted')) if bills_due else False

    def action_view_bills(self):
        self.ensure_one()
        result = {
            "name": "Bills",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', self.bill_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_view_bills_due(self):
        self.ensure_one()
        result = {
            "name": "Due Bills",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', self.bill_ids_due.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    # RFQs lines (services requested) functions
    @api.depends('rfq_ids.order_line')
    def _get_rfqol_ids(self):
        for record in self:
            rfq_lines = record.env['purchase.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.order_id.state in ('draft', 'sent','to approve'))
            record.rfqol_ids = rfq_lines if rfq_lines else False
            record.rfqol_ids_count = len(rfq_lines) if rfq_lines else False
            record.rfqol_ids_amount_untaxed = sum(
                line.price_subtotal for line in rfq_lines) if rfq_lines else False
            record.rfqol_ids_amount_tax = sum(line.price_tax for line in rfq_lines) if rfq_lines else False
            record.rfqol_ids_amount_total = sum(
                line.price_total for line in rfq_lines) if rfq_lines else False

    # purchase order lines (services received) functions
    @api.depends('po_ids.order_line')
    def _get_pol_ids(self):
        for record in self:
            purchase_order_lines = record.env['purchase.order.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.order_id.state in ('purchase', 'done'))
            record.pol_ids = purchase_order_lines if purchase_order_lines else False
            record.pol_ids_count = len(purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_untaxed = sum(
                line.price_subtotal for line in purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_tax = sum(line.price_tax for line in purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_total = sum(
                line.price_total for line in purchase_order_lines) if purchase_order_lines else False
    
    # Bills lines (services invoiced) functions
    @api.depends('bill_ids.invoice_line_ids')
    def _get_bol_ids(self):
        for record in self:
            bill_lines = record.env['account.move.line'].sudo().search(
                [('reference_document', '=', str(record._name) + ',' + str(record.id))]).filtered(
                lambda r: r.move_id.move_type in ('in_invoice', 'in_refund') and r.move_id.state == 'posted')
            record.bol_ids = bill_lines if bill_lines else False
            record.bol_ids_count = len(bill_lines) if bill_lines else False
            record.bol_ids_amount_untaxed = sum(
                line.price_subtotal for line in bill_lines) if bill_lines else False
            record.bol_ids_amount_tax = sum(line.tax_base_amount for line in bill_lines) if bill_lines else False
            record.bol_ids_amount_total = sum(
                line.price_total for line in bill_lines) if bill_lines else False
