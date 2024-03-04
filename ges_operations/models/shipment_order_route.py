# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class ShipmentOrderRoute(models.Model):
    _name = "shipment.order.route"
    _description = "Shipment Order Route"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    shipment_order_id = fields.Many2one('shipment.order', string="Shipment Order")

    company_id = fields.Many2one(string="Company", related="shipment_order_id.company_id")
    currency_id = fields.Many2one(string="Currency", related="shipment_order_id.currency_id")

    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string="Color", related="shipment_order_id.color")
    sequence = fields.Integer(string="Sequence")
    
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())

    # general order fields
    leg_type = fields.Selection(([('main-carriage', 'Main-Carriage'),('pre-carriage', 'Pre-Carriage'), ('on-carriage', 'On-Carriage')]), string='Leg Type', default="pre-carriage")
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', default="ocean")
    
    @api.depends('transport')
    @api.onchange('transport')
    def _update_address_types(self):
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
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict', related="shipment_order_id.partner_id")
    partner_contact_id = fields.Many2one('res.partner', string="Customer Contact", ondelete='restrict', related="shipment_order_id.partner_contact_id")
    customer_country = fields.Many2one(related='partner_contact_id.country_id', string="Customer Country")
    customer_email = fields.Char(related='partner_contact_id.email', string="Customer Email")
    customer_phone = fields.Char(related='partner_contact_id.phone', string="Customer Phone")
    customer_mobile = fields.Char(related='partner_contact_id.mobile', string="Customer Mobile")

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_partner_contact_id(self):        
        self.partner_contact_id = False

    # First Notify fields
    first_notify_id = fields.Many2one('res.partner', string='1st Notify', ondelete='restrict', related="shipment_order_id.first_notify_id")
    first_notify_contact_id = fields.Many2one('res.partner', string="1st Notify Contact", ondelete='restrict', related="shipment_order_id.first_notify_contact_id")
    first_notify_country = fields.Many2one(related='first_notify_contact_id.country_id', string="1st Notify Country")
    first_notify_email = fields.Char(related='first_notify_contact_id.email', string="1st Notify Email")
    first_notify_phone = fields.Char(related='first_notify_contact_id.phone', string="1st Notify Phone")
    first_notify_mobile = fields.Char(related='first_notify_contact_id.mobile', string="1st Notify Mobile")

    @api.depends('first_notify_id')
    @api.onchange('first_notify_id')
    def _update_first_notify_contact_id(self):
        self.first_notify_contact_id = False

    # Second Notify fields
    second_notify_id = fields.Many2one('res.partner', string='2nd Notify', ondelete='restrict', related="shipment_order_id.second_notify_id")
    second_notify_contact_id = fields.Many2one('res.partner', string="2nd Notify Contact", ondelete='restrict', related="shipment_order_id.second_notify_contact_id")
    second_notify_country = fields.Many2one(related='second_notify_contact_id.country_id', string="2nd Notify Country")
    second_notify_email = fields.Char(related='second_notify_contact_id.email', string="2nd Notify Email")
    second_notify_phone = fields.Char(related='second_notify_contact_id.phone', string="2nd Notify Phone")
    second_notify_mobile = fields.Char(related='second_notify_contact_id.mobile', string="2nd Notify Mobile")

    @api.depends('second_notify_id')
    @api.onchange('second_notify_id')
    def _update_second_notify_contact_id(self):
        self.second_notify_contact_id = False

    # Shipper
    shipper_id = fields.Many2one('res.partner', domain=[], ondelete='restrict', related="shipment_order_id.shipper_id")
    shipper_contact_id = fields.Many2one('res.partner', string="Shipper Contact", ondelete='restrict', related="shipment_order_id.shipper_contact_id")
    shipper_country = fields.Many2one(related='shipper_contact_id.country_id', string="Shipper Country")
    shipper_email = fields.Char(related='shipper_contact_id.email', string="Shipper Email")
    shipper_phone = fields.Char(related='shipper_contact_id.phone', string="Shipper Phone")
    shipper_mobile = fields.Char(related='shipper_contact_id.mobile', string="Shipper Mobile")

    @api.depends('shipper_id')
    @api.onchange('shipper_id')
    def _update_shipper_contact_id(self):
        self.shipper_contact_id = False

    # Consignee
    consignee_id = fields.Many2one('res.partner', domain=[], ondelete='restrict', related="shipment_order_id.consignee_id")
    consignee_contact_id = fields.Many2one('res.partner', string="Consignee Contact", ondelete='restrict', related="shipment_order_id.consignee_contact_id")
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
    no_bill = fields.Selection([('zero', '(0) ZERO'), ('three', '(3) THREE'), ('surrender', 'SURRENDER')])
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

            elif record.origin_address_type == 'door':
                if record.origin_address_id:
                    record.origin_country_id = record.origin_address_id.country_id
                    record.origin_state_id = record.origin_address_id.state_id
                    record.origin_city_id = record.origin_address_id.city_id
                    record.origin_zip_code = record.origin_address_id.zip_code
                    record.origin_street = record.origin_address_id.street
                    record.origin_street2 = record.origin_address_id.street2
                    record.origin_code = record.origin_address_id.code

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

            elif record.destination_address_type == 'door':
                if record.destination_address_id:
                    record.destination_country_id = record.destination_address_id.country_id
                    record.destination_state_id = record.destination_address_id.state_id
                    record.destination_city_id = record.destination_address_id.city_id
                    record.destination_zip_code = record.destination_address_id.zip_code
                    record.destination_street = record.destination_address_id.street
                    record.destination_street2 = record.destination_address_id.street2
                    record.destination_code = record.destination_address_id.code

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


    # order packages

    freight_package_ids = fields.One2many('shipment.order.package', 'route_id')

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

