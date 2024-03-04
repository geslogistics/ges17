# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class ShipmentOrder(models.Model):
    _name = "shipment.order"
    _description = "Shipment Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')

    # record fields
    active = fields.Boolean(default=True, string='Active', tracking=True)
    color = fields.Integer('Color')
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())
    state_selection = [('new', 'Draft'), ('quotation', 'Quotation Sent'), ('booked', 'Booked'), ('inprogress', 'In Progress'), ('confirmed', 'Confirmed'), ('intransit', 'In Transit'), ('delivered', 'Delivered'), ('closed', 'Closed'), ('cancel', 'Cancelled')]
    state = fields.Selection(state_selection, string='Status', copy=False, tracking=True, default='new')

    # general order fields
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    category = fields.Selection([('direct','Direct'),('house','House'),('master','Master')], string="Category", default="direct", tracking=True)
    direction = fields.Selection(([('import', 'Import'), ('export', 'Export')]), string='Direction', default="export")
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', default="ocean")
    move_type = fields.Selection([('d2d','Door-to-Door'),('d2p','Door-to-Port'),('p2p','Port-to-Port'),('p2d','Port-to-Door')], string="Move Type")
    
    """
    @api.depends('transport','move_type')
    @api.onchange('transport','move_type')
    def _update_address_types(self):
        if self self.transport == 'road':
            self.origin_address_type = 'door'
            self.destination_address_type = 'door'
            self.pickup_option = False
            self.delivery_option = False
        elif self.transport in ['air','ocean','rail']:
            if self.move_type == 'd2d':
                self.origin_address_type = 'port'
                self.destination_address_type = 'port'
                self.pickup_option = True
                self.delivery_option = True
            elif self.move_type == 'd2p':
                self.origin_address_type = 'door'
                self.destination_address_type = 'port'
                self.pickup_option = True
                self.delivery_option = False
            elif self.move_type == 'p2p':
                self.origin_address_type = 'port'
                self.destination_address_type = 'port'
                self.pickup_option = False
                self.delivery_option = False
            elif self.move_type == 'p2d':
                self.origin_address_type = 'port'
                self.destination_address_type = 'door'
                self.pickup_option = False
                self.delivery_option = True
    
    """

    @api.depends('transport')
    @api.onchange('transport')
    def _update_address_types2(self):
        if self.transport in ['air','ocean','rail']:
            self.origin_address_type = 'port'
            self.destination_address_type = 'port'
        elif self.transport == 'road':
            self.origin_address_type = 'door'
            self.destination_address_type = 'door'


    shipment_mode = fields.Selection([('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
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
         ('others', 'Others')], string="Shipment Mode")
         
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
         ('loose_cargo_others', 'Loose Cargo > Others')], string="Ocean Shipment Mode", default="general_cargo_full_container_load_fcl")
    air_shipment_mode = fields.Selection(
        [('general_cargo_full_container_load_fcl', 'General Cargo > Full Container Load (FCL)'),
         ('general_cargo_less_than_container_load_lcl', 'General Cargo > Less Than Container Load (LCL)'),
         ('general_cargo_break-bulk', 'General Cargo > Break-bulk'),
         ('special_cargo_live_animal', 'Special Cargo > Live Animal'),
         ('special_cargo_perishable_cargo', 'Special Cargo > Perishable Cargo'),
         ('special_cargo_mail_cargo', 'Special Cargo > Mail Cargo'),
         ('special_cargo_human_remains,_tissue,_and_organ_cargo',
          'Special Cargo > Human Remains, Tissue, and Organ Cargo'),
         ('special_cargo_others', 'Special Cargo > Others')], string="Air Shipment Mode", default="general_cargo_full_container_load_fcl")
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
         ('others', 'Others'), ], string="Road Shipment Mode", default="full_truck_load_ftl_flatbed_trailer")
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
         ('others', 'Others')], string="Rail Shipment Mode", default="full_truck_load_ftl_flatbed_trailer")


    # Customer fields
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict')
    partner_contact_id = fields.Many2one('res.partner', string="Customer Contact", ondelete='restrict')
    customer_country = fields.Many2one(related='partner_contact_id.country_id', string="Customer Country")
    customer_email = fields.Char(related='partner_contact_id.email', string="Customer Email")
    customer_phone = fields.Char(related='partner_contact_id.phone', string="Customer Phone")
    customer_mobile = fields.Char(related='partner_contact_id.mobile', string="Customer Mobile")

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_partner_contact_id(self):        
        self.partner_contact_id = False

    is_customer_agent = fields.Boolean(string="Is Agent?")

    # First Notify fields
    first_notify_id = fields.Many2one('res.partner', string='1st Notify', ondelete='restrict')
    first_notify_contact_id = fields.Many2one('res.partner', string="1st Notify Contact", ondelete='restrict')
    first_notify_country = fields.Many2one(related='first_notify_contact_id.country_id', string="1st Notify Country")
    first_notify_email = fields.Char(related='first_notify_contact_id.email', string="1st Notify Email")
    first_notify_phone = fields.Char(related='first_notify_contact_id.phone', string="1st Notify Phone")
    first_notify_mobile = fields.Char(related='first_notify_contact_id.mobile', string="1st Notify Mobile")

    @api.depends('first_notify_id')
    @api.onchange('first_notify_id')
    def _update_first_notify_contact_id(self):
        self.first_notify_contact_id = False

    # Second Notify fields
    second_notify_id = fields.Many2one('res.partner', string='2nd Notify', ondelete='restrict')
    second_notify_contact_id = fields.Many2one('res.partner', string="2nd Notify Contact", ondelete='restrict')
    second_notify_country = fields.Many2one(related='second_notify_contact_id.country_id', string="2nd Notify Country")
    second_notify_email = fields.Char(related='second_notify_contact_id.email', string="2nd Notify Email")
    second_notify_phone = fields.Char(related='second_notify_contact_id.phone', string="2nd Notify Phone")
    second_notify_mobile = fields.Char(related='second_notify_contact_id.mobile', string="2nd Notify Mobile")

    @api.depends('second_notify_id')
    @api.onchange('second_notify_id')
    def _update_second_notify_contact_id(self):
        self.second_notify_contact_id = False

    # Shipper
    shipper_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    shipper_contact_id = fields.Many2one('res.partner', string="Shipper Contact", ondelete='restrict')
    shipper_country = fields.Many2one(related='shipper_contact_id.country_id', string="Shipper Country")
    shipper_email = fields.Char(related='shipper_contact_id.email', string="Shipper Email")
    shipper_phone = fields.Char(related='shipper_contact_id.phone', string="Shipper Phone")
    shipper_mobile = fields.Char(related='shipper_contact_id.mobile', string="Shipper Mobile")

    @api.depends('shipper_id')
    @api.onchange('shipper_id')
    def _update_shipper_contact_id(self):
        self.shipper_contact_id = False

    # Consignee
    consignee_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    consignee_contact_id = fields.Many2one('res.partner', string="Consignee Contact", ondelete='restrict')
    consignee_country = fields.Many2one(related='consignee_contact_id.country_id', string="Consignee Country")
    consignee_email = fields.Char(related='consignee_contact_id.email', string="Consignee Email")
    consignee_phone = fields.Char(related='consignee_contact_id.phone', string="Consignee Phone")
    consignee_mobile = fields.Char(related='consignee_contact_id.mobile', string="Consignee Mobile")

    @api.depends('consignee_id')
    @api.onchange('consignee_id')
    def _update_consignee_contact_id(self):
        self.consignee_contact_id = False

    # Agent
    agent_id = fields.Many2one('res.partner', domain=[], ondelete='restrict')
    agent_contact_id = fields.Many2one('res.partner', string="Agent Contact", ondelete='restrict')
    agent_country = fields.Many2one(related='agent_contact_id.country_id', string="Agent Country")
    agent_email = fields.Char(related='agent_contact_id.email', string="Agent Email")
    agent_phone = fields.Char(related='agent_contact_id.phone', string="Agent Phone")
    agent_mobile = fields.Char(related='agent_contact_id.mobile', string="Agent Mobile")
    
    bl_document_type = fields.Selection(
        [('Draft', 'DRAFT'), ('Copy', 'COPY NON NEGOTIABLE '), ('original', 'ORIGINAL'),
         ('telex_release', 'Telex Release')],
        string="B/L Document Type")
    freight_payable = fields.Char(string="Freight Payable At")
    no_bill = fields.Selection([('zero', '(0) ZERO'), ('three', '(3) THREE'), ('surrender', 'SURRENDER')], string="Number of B(s)/L")
    freight_amount = fields.Monetary(string="Freight Amount")
    si_issue_date = fields.Date(string="S/I Issue Date")

    @api.depends('agent_id')
    @api.onchange('agent_id')
    def _update_agent_contact_id(self):
        self.agent_contact_id = False
    
    #user and unit fields
    order_user_id = fields.Many2one('res.users', string='Order User', index=True, default=lambda self: self.env.user)
    order_ou_id = fields.Many2one(comodel_name='operating.unit', string="Order Unit", related='order_user_id.default_operating_unit_sales_id', store=True)   

    assigned_user_id = fields.Many2one('res.users', string="Sales Ops User")
    assigned_ou_id = fields.Many2one('operating.unit', string="Sales Ops Unit", related="assigned_user_id.default_operating_unit_sales_ops_id")

    sales_user_id = fields.Many2one(comodel_name='res.users', string="Sales User", related='partner_id.sales_user_id', store=True)
    sales_ou_id = fields.Many2one(comodel_name='operating.unit', string="Sales Unit", related='partner_id.sales_ou_id', store=True)    

    #origin fields
    origin_address_type = fields.Selection([('port','Port'),('door','Door')])
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
        if self.origin_address_type == 'port':
            self.origin_address_id = False
        elif self.origin_address_type == 'door':
            self.origin_port_id = False
            self.pickup_option = False

    @api.depends('origin_address_type','origin_port_id','origin_address_id')
    @api.onchange('origin_address_type','origin_port_id','origin_address_id')
    def _compute_origin_address(self):
        self.origin_country_id = False
        self.origin_state_id = False
        self.origin_city_id = False
        self.origin_zip_code = False
        self.origin_street = False
        self.origin_street2 = False
        self.origin_code = False

        if self.origin_address_type == 'port':
            if self.origin_port_id:
                self.origin_country_id = self.origin_port_id.country_id
                self.origin_state_id = self.origin_port_id.state_id
                self.origin_city_id = self.origin_port_id.city_id
                self.origin_zip_code = self.origin_port_id.zip_code
                self.origin_street = self.origin_port_id.street
                self.origin_street2 = self.origin_port_id.street2
                self.origin_code = self.origin_port_id.code

        elif self.origin_address_type == 'door':
            if self.origin_address_id:
                self.origin_country_id = self.origin_address_id.country_id
                self.origin_state_id = self.origin_address_id.state_id
                self.origin_city_id = self.origin_address_id.city_id
                self.origin_zip_code = self.origin_address_id.zip_code
                self.origin_street = self.origin_address_id.street
                self.origin_street2 = self.origin_address_id.street2
                self.origin_code = self.origin_address_id.code

    # origin contact fields
    origin_contact_id = fields.Many2one('res.partner', string="Loading Contact", ondelete='restrict')
    origin_contact_country = fields.Many2one(related='origin_contact_id.country_id', string="Loading Contact Country")
    origin_contact_email = fields.Char(related='origin_contact_id.email', string="Loading Contact Email")
    origin_contact_phone = fields.Char(related='origin_contact_id.phone', string="Loading Contact Phone")
    origin_contact_mobile = fields.Char(related='origin_contact_id.mobile', string="Loading Contact Mobile")
    
    @api.depends('origin_address_id')
    @api.onchange('origin_address_id')
    def _update_origin_contact_id(self):
        self.origin_contact_id = False

    #destination fields
    destination_address_type = fields.Selection([('port','Port'),('door','Door')])
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
        if self.destination_address_type == 'port':
            self.destination_address_id = False
        elif self.destination_address_type == 'door':
            self.destination_port_id = False
            self.delivery_option = False

    @api.depends('destination_address_type','destination_port_id','destination_address_id')
    @api.onchange('destination_address_type','destination_port_id','destination_address_id')
    def _compute_destination_address(self):
        self.destination_country_id = False
        self.destination_state_id = False
        self.destination_city_id = False
        self.destination_zip_code = False
        self.destination_street = False
        self.destination_street2 = False
        self.destination_code = False

        if self.destination_address_type == 'port':
            if self.destination_port_id:
                self.destination_country_id = self.destination_port_id.country_id
                self.destination_state_id = self.destination_port_id.state_id
                self.destination_city_id = self.destination_port_id.city_id
                self.destination_zip_code = self.destination_port_id.zip_code
                self.destination_street = self.destination_port_id.street
                self.destination_street2 = self.destination_port_id.street2
                self.destination_code = self.destination_port_id.code

        elif self.destination_address_type == 'door':
            if self.destination_address_id:
                self.destination_country_id = self.destination_address_id.country_id
                self.destination_state_id = self.destination_address_id.state_id
                self.destination_city_id = self.destination_address_id.city_id
                self.destination_zip_code = self.destination_address_id.zip_code
                self.destination_street = self.destination_address_id.street
                self.destination_street2 = self.destination_address_id.street2
                self.destination_code = self.destination_address_id.code

    # destination contact fields
    destination_contact_id = fields.Many2one('res.partner', string="Discharge Contact", ondelete='restrict')
    destination_contact_country = fields.Many2one(related='destination_contact_id.country_id', string="Discharge Contact Country")
    destination_contact_email = fields.Char(related='destination_contact_id.email', string="Discharge Contact Email")
    destination_contact_phone = fields.Char(related='destination_contact_id.phone', string="Discharge Contact Phone")
    destination_contact_mobile = fields.Char(related='destination_contact_id.mobile', string="Discharge Contact Mobile")

    @api.depends('destination_address_id')
    @api.onchange('destination_address_id')
    def _update_destination_contact_id(self):
        self.destination_contact_id = False

    #pickup fields
    pickup_option = fields.Boolean(string="Pickup?")
    pickup_address_id = fields.Many2one('freight.address', string="Pickup Location")
    pickup_country_id = fields.Many2one('res.country', string="Pickup Country", compute="_compute_pickup_address", store=True, copy=False)
    pickup_state_id = fields.Many2one('res.country.state', string="Pickup State", compute="_compute_pickup_address", store=True, copy=False)
    pickup_city_id = fields.Many2one('res.city', string="Pickup City", compute="_compute_pickup_address", store=True, copy=False)
    pickup_zip_code = fields.Char(string="Pickup Zip Code", compute="_compute_pickup_address", store=True, copy=False)
    pickup_street = fields.Char(string="Pickup Street 1", compute="_compute_pickup_address", store=True, copy=False)
    pickup_street2 = fields.Char(string="Pickup Street 2", compute="_compute_pickup_address", store=True, copy=False)
    pickup_code = fields.Char(string="Pickup Address Code", compute="_compute_pickup_address", store=True, copy=False)

    @api.depends('pickup_option')
    @api.onchange('pickup_option')
    def _reset_pickup_address(self):
        if self.pickup_option == False:
            self.pickup_address_id = False

    @api.depends('pickup_address_id')
    @api.onchange('pickup_address_id')
    def _compute_pickup_address(self):
        self.pickup_country_id = False
        self.pickup_state_id = False
        self.pickup_city_id = False
        self.pickup_zip_code = False
        self.pickup_street = False
        self.pickup_street2 = False
        self.pickup_code = False

        if self.pickup_address_id:
            self.pickup_country_id = self.pickup_address_id.country_id
            self.pickup_state_id = self.pickup_address_id.state_id
            self.pickup_city_id = self.pickup_address_id.city_id
            self.pickup_zip_code = self.pickup_address_id.zip_code
            self.pickup_street = self.pickup_address_id.street
            self.pickup_street2 = self.pickup_address_id.street2
            self.pickup_code = self.pickup_address_id.code

    #delivery fields
    delivery_option = fields.Boolean(string="Delivery?")
    delivery_address_id = fields.Many2one('freight.address', string="Delivery Location")
    delivery_country_id = fields.Many2one('res.country', string="Delivery Country", compute="_compute_delivery_address", store=True, copy=False)
    delivery_state_id = fields.Many2one('res.country.state', string="Delivery State", compute="_compute_delivery_address", store=True, copy=False)
    delivery_city_id = fields.Many2one('res.city', string="Delivery City", compute="_compute_delivery_address", store=True, copy=False)
    delivery_zip_code = fields.Char(string="Delivery Zip Code", compute="_compute_delivery_address", store=True, copy=False)
    delivery_street = fields.Char(string="Delivery Street 1", compute="_compute_delivery_address", store=True, copy=False)
    delivery_street2 = fields.Char(string="Delivery Street 2", compute="_compute_delivery_address", store=True, copy=False)
    delivery_code = fields.Char(string="Delivery Address Code", compute="_compute_delivery_address", store=True, copy=False)

    @api.depends('delivery_option')
    @api.onchange('delivery_option')
    def _reset_delivery_address(self):
        if self.delivery_option == False:
            self.delivery_address_id = False

    @api.depends('delivery_address_id')
    @api.onchange('delivery_address_id')
    def _compute_delivery_address(self):
        self.delivery_country_id = False
        self.delivery_state_id = False
        self.delivery_city_id = False
        self.delivery_zip_code = False
        self.delivery_street = False
        self.delivery_street2 = False
        self.delivery_code = False

        if self.delivery_address_id:
            self.delivery_country_id = self.delivery_address_id.country_id
            self.delivery_state_id = self.delivery_address_id.state_id
            self.delivery_city_id = self.delivery_address_id.city_id
            self.delivery_zip_code = self.delivery_address_id.zip_code
            self.delivery_street = self.delivery_address_id.street
            self.delivery_street2 = self.delivery_address_id.street2
            self.delivery_code = self.delivery_address_id.code
    
    # tracking
    tracking_number = fields.Char('Tracking Number')

    # general information fields
    distance = fields.Integer(string='Distance')
    bl_number = fields.Char(string="B/L")
    special_instructions = fields.Text(string="Special Instruction")
    contact_place_of_receipt = fields.Selection([('Shipper', 'Shipper'), ('Consignee', 'Consignee')], string="Place of Receipt", default="Consignee")
    contact_place_of_delivery = fields.Selection([('Shipper', 'Shipper'), ('Consignee', 'Consignee')], string="Place of Delivery", default="Consignee")
    incoterms_id = fields.Many2one('freight.incoterms', string='Incoterms', ondelete='restrict')
    incoterms_code = fields.Char(related="incoterms_id.code")
    delivery_terms = fields.Selection([('pp', 'Prepaid (PP)'), ('cc', 'Collect (CC)'),('cp','Prepaid/Collect (CP)')], string="Delivery Terms")
    delivery_terms_code = fields.Char("Delivery Terms Code", compute="_get_delivery_terms_code")
    is_dangerous = fields.Boolean(string="Dangerous Goods")
    notes = fields.Text('Notes')

    # Carriage Dates
    pickup_datetime = fields.Datetime('Est. Pickup')
    arrival_datetime = fields.Datetime('Est. Arrival')

    


    @api.onchange('ocean_shipment_mode','air_shipment_mode','road_shipment_mode','rail_shipment_mode')
    def _onchange_shipment_mode(self):
        if self.transport == 'ocean':
            self.shipment_mode = self.ocean_shipment_mode
        elif self.transport == 'air':
            self.shipment_mode = self.air_shipment_mode
        elif self.transport == 'road':
            self.shipment_mode = self.road_shipment_mode
        elif self.transport == 'rail':
            self.shipment_mode = self.rail_shipment_mode

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

    
    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            if values.get('transport') == 'air':
                air_pre = "GES/SHO"
                values['name'] = air_pre + self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
            elif values.get('transport') == 'ocean':
                ocean_pre = "GES/SHO"
                values['name'] = ocean_pre + self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
            elif values.get('transport') == 'road':
                road_pre = "GES/SHO"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
            elif values.get('transport') == 'rail':
                road_pre = "GES/SHO"
                values['name'] = road_pre + self.env['ir.sequence'].next_by_code('shipment.order') or _('New')
        if values.get('name', False) and not values.get('tracking_number', False):
            values['tracking_number'] = values.get('name', False)

        result = super(ShipmentOrder, self).create(values)
        
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


        result = super(ShipmentOrder, self).write(values)
        return result

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


    def create_new_address(self):
        return {
            # 'name': self.order_id,
            'res_model': 'freight.address',
            'type': 'ir.actions.act_window',
            'context': {'default_partner_id': self.partner_id.id},
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }



    # order packages

    freight_package_ids = fields.One2many('shipment.order.package', 'shipment_order_id')

    ## Total Net, Gross and Volume
    package_total_gross = fields.Float(compute="_compute_total_gross_net_volume")
    package_total_net = fields.Float(compute="_compute_total_gross_net_volume")
    package_total_volume = fields.Float(compute="_compute_total_gross_net_volume")

    @api.depends('freight_package_ids')
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



    #air carriage fields
    airline_partner_id = fields.Many2one('res.partner', string="Airline Account")
    airline_id = fields.Many2one('freight.airline', string='Airline', domain="[('partner_id','=',airline_partner_id)]")
    mawb_no = fields.Char('MAWB No')
    flight_no = fields.Char('Flight No')

    # Mask And Numbers
    mask_numbers = fields.Text(string="Mask and Numbers")
    desc_pkg = fields.Text(string="Description and Packages & Goods Particulars Furnished by Shipper")
    measurement = fields.Text(string="Measurement")
    remark = fields.Text(string="Remarks")


    # Ocean
    carrier_partner_id = fields.Many2one('res.partner', string="Carrier Account")
    vessel_id = fields.Many2one('freight.vessel', string='Vessel', domain="[('partner_id','=',carrier_partner_id)]")
    transhipment_port = fields.Many2one('freight.port', string="Transhipment Port")
    obl = fields.Char('OBL No.', help='Original Bill Of Landing')
    voyage_no = fields.Char('Voyage No')

    # rail
    railway_partner_id = fields.Many2one('res.partner', string="Railway Account")
    railway_id = fields.Many2one('freight.railway', string='Railway', domain="[('partner_id','=',railway_partner_id)]")
    train_no = fields.Char('Train No')
    car_no = fields.Char('Car No')
    
    # Land
    vehicle_partner_id = fields.Many2one('res.partner', string="Truck Account")
    truck_ref = fields.Char('CMR/RWB')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', domain="[('is_freight_shipment','=',True),('partner_id','=',vehicle_partner_id)]")
    

    # Insurance
    is_freight_insurance = fields.Boolean(string='Is Freight Insurance')
    policy_no = fields.Char(string='Policy No.')
    policy_partner_id = fields.Many2one('res.partner')
    date = fields.Date(string='Issue Date')
    issue_by = fields.Char(string='Issued By')
    policy_name = fields.Char(string='Policy Name')
    policy_holder_id = fields.Many2one(related="consignee_id", string="Policy Holder")
    term = fields.Html(string='Insurance Terms')
    risk_ids = fields.Many2many('freight.policy.risk', string='Risk Covered')
    policy_added = fields.Boolean(string='Policy Added')


    # routes
    route_ids = fields.One2many('shipment.order.route','shipment_order_id', string="Routes")
    pre_route_ids = fields.One2many('shipment.order.route', compute="_compute_routes", string="Pre-Carriage Routes")
    on_route_ids = fields.One2many('shipment.order.route', compute="_compute_routes", string="On-Carriage Routes")
    
    @api.depends('route_ids')
    @api.onchange('route_ids')
    def _compute_routes(self):
        for record in self:
            record.pre_route_ids = record.route_ids.filtered(lambda r: r.leg_type == 'pre-carriage')
            record.on_route_ids = record.route_ids.filtered(lambda r: r.leg_type == 'on-carriage')


    # services
    service_ids = fields.One2many('shipment.order.service','shipment_order_id', string="Services")
    pre_service_ids = fields.One2many('shipment.order.service', compute="_compute_services", string="Pre-Carriage Services")
    on_service_ids = fields.One2many('shipment.order.service', compute="_compute_services", string="On-Carriage Services")

    @api.depends('service_ids')
    @api.onchange('service_ids')
    def _compute_services(self):
        for record in self:
            record.pre_service_ids = record.service_ids.filtered(lambda r: r.service_at == 'pre-carriage')
            record.on_service_ids = record.service_ids.filtered(lambda r: r.service_at == 'on-carriage')

    def action_add_route(self):
        result = {
            "name": "Add a Route",
            "type": "ir.actions.act_window",
            "res_model": "shipment.order.route",
            "view_mode": "form",
            "target":"new",
            "context": {
                "default_shipment_order_id": self.id,
                },
        }
        return result
    
    def action_add_service(self):
        result = {
            "name": "Add a Service",
            "type": "ir.actions.act_window",
            "res_model": "shipment.order.service",
            "view_mode": "form",
            "target":"new",
            "context": {
                "default_shipment_order_id": self.id,
                },
        }
        return result


    # Finance and Accounting

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
