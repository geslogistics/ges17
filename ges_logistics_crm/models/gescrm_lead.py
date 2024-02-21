# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from werkzeug import urls

class GESCRMLead(models.Model):
    _name = 'gescrm.lead'
    _description = "CRM Lead"
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin']
    _name_rec = 'legal_name'

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)


    assigned_user_id = fields.Many2one('res.users', string='Assigned User', compute='_compute_user_ou', store=True)
    assigned_ou_id = fields.Many2one('operating.unit', string='Assigned Unit', compute='_compute_user_ou', store=True)
    @api.depends('partner_type','sales_user_id','sales_ou_id','procurement_user_id','procurement_ou_id')
    def _compute_user_ou(self):
        for record in self:
            if record.partner_type == 'customer':
                record.assigned_user_id = record.sales_user_id
                record.assigned_ou_id = record.sales_ou_id
            else:
                record.assigned_user_id = record.procurement_user_id
                record.assigned_ou_id = record.procurement_ou_id

    referral_user_id = fields.Many2one('res.users', string='Referral User', compute='_compute_referral_user_ou', store=True)
    referral_ou_id = fields.Many2one('operating.unit', string='Referral Unit', compute='_compute_referral_user_ou', store=True)
    @api.depends('partner_type','sales_referral_user_id','sales_referral_ou_id','procurement_referral_user_id','procurement_referral_ou_id')
    def _compute_referral_user_ou(self):
        for record in self:
            if record.partner_type == 'customer':
                record.referral_user_id = record.sales_referral_user_id
                record.referral_ou_id = record.sales_referral_ou_id
            else:
                record.referral_user_id = record.procurement_referral_user_id
                record.referral_ou_id = record.procurement_referral_ou_id



    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, readonly=True,
                                  default=lambda self: self.env.company.currency_id.id)
    
    ## GES Lead Fields
    name = fields.Char(string="Opportunity")
    stage_id = fields.Many2one('gescrm.lead.stage', string='Stage', index=True, tracking=True, compute='_compute_stage_id', readonly=False, store=True, copy=False, ondelete='restrict')

    @api.depends('partner_type')
    def _compute_stage_id(self):
        for record in self:
            if not record.stage_id:
                record.stage_id = self.env['gescrm.lead.stage'].search([], order="sequence, id", limit=1).id



    partner_type = fields.Selection([('customer','Customer'),('vendor','Vendor')], default='customer', string="Partner Type")
    
    AVAILABLE_PRIORITIES = [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
    ]
    
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    tag_ids = fields.Many2many(
        'crm.tag', 'crm_gestag_rel', 'geslead_id', 'tag_id', string='Tags',
        help="Classify and analyze your lead/opportunity categories like: Training, Service")
    color = fields.Integer('Color Index', default=0)

    description = fields.Html('Notes')
    active = fields.Boolean('Active', default=True, tracking=True)

    campaign_id = fields.Many2one(ondelete='set null')
    medium_id = fields.Many2one(ondelete='set null')
    source_id = fields.Many2one(ondelete='set null')


    expected_revenue = fields.Monetary('Expected Revenue', tracking=True)
    probability = fields.Float('Probability')
    date_deadline = fields.Date('Expected Closing')
    date_closed = fields.Datetime('Closed Date', readonly=True, copy=False)
    date_open = fields.Datetime('Assignment Date', compute='_compute_date_open', readonly=True, store=True)

    @api.depends('partner_type','sales_user_id','procurement_user_id')
    def _compute_date_open(self):
        for record in self:
            if record.partner_type == 'customer':
                record.date_open = self.env.cr.now() if record.sales_user_id else False
            elif record.partner_type == 'vendor':
                record.date_open = self.env.cr.now() if record.procurement_user_id else False


    ## CONTACT PERSON FIELDS
    contact_name = fields.Char(string="Contact Name")
    contact_function = fields.Char("Job Position")
    contact_title = fields.Many2one('res.partner.title', string="Title")
    contact_email = fields.Char()
    contact_phone = fields.Char(unaccent=False)
    contact_mobile = fields.Char(unaccent=False)

    ## COMMON KYC FIELDS
    company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], default="company")
    legal_name = fields.Char(string='Name', help="Official / Legal English Name")
    name_alt_lang = fields.Char(string='Name (AR)', help="Official / Legal Name (AR)")
    trade_name = fields.Char(string='Trading Name', translate=True, help="if different from Legal Entity Name")
    trade_name_alt_lang = fields.Char(string='Trading Name (AR)', translate=True, help="if different from Legal Entity Name")
    
    category_id = fields.Many2many('res.partner.category', 'partner_tags_geslead', 'geslead_partner_id' ,'geslead_category_id', string='Tags', help="Account tags can be used for filtering and reporting")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    city_id = fields.Many2one(comodel_name='res.city', string='City')
    country_enforce_cities = fields.Boolean(related='country_id.enforce_cities')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(string="Country Code", related='country_id.code')
    l10n_sa_edi_building_number = fields.Char(string="Building Number")
    l10n_sa_edi_plot_identification = fields.Char(string="Plot Identification")

    email = fields.Char()
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)
    website = fields.Char('Website Link')
    company_registry = fields.Char(string="CR/ID Number", help="The official CR/ID number. Use it if it is different from the Tax ID. It must be unique across all partners of a same country")
    company_registry_expiry_date = fields.Date(string="CR/ID Expiry")
    vat = fields.Char(string='Tax ID', help="i.e. VAT Number")
    ref = fields.Char(string='Reference', help="Internal reference to be used for the account")

    ## KYC - Companies
    legal_type = fields.Selection([('establishment','Establishment'),('joint_liability','Joint Liability Company'),('limited_partnership','Limited Partnership Company'),('simple_joint','Simple Joint Stock Company'),('closed_joint','Closed Joint Stock Company'),('public','Public Joint Stock Company'),('llc','Limited Liability Company'),('one_llc','One Person Limited Liability Company')], default="llc")
    industry_id = fields.Many2one('res.partner.industry', 'Industry')
    paidup_capital = fields.Monetary("Paid-up Capital", help="As per registration")
    ownership_structure = fields.Html("Ownership Structure", help="List of owners and their ownership percentages")
    management_structure = fields.Html("Management Structure", help="List of account's management team members")
    year_founded = fields.Char("Year Founded")

    ## KYC - Individuals
    function = fields.Char("Job Position")
    title = fields.Many2one('res.partner.title', string="Title")

    @api.onchange('company_type')
    @api.depends('company_type')
    def clear_individual_fields(self):
        if self.company_type == 'company':
            self.function = False
            self.title = False

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.zip = self.city_id.zipcode
            self.state_id = self.city_id.state_id
        elif self._origin:
            self.city = False
            self.zip = False
            self.state_id = False

    
    #### CUSTOMER FIELDS

    # Customer CRM Fields
    
    sales_user_id = fields.Many2one('res.users', string='Sales User')
    sales_ou_id = fields.Many2one('operating.unit', string='Sales Unit', compute='_compute_sales_ou_id', store=True, readonly=False, index=True)

    
    
    @api.depends('sales_user_id')
    @api.onchange('sales_user_id')
    def _compute_sales_ou_id(self):
        for record in self:
            record.sales_ou_id = False
            if record.sales_user_id:
                record.sales_ou_id = record.sales_user_id.default_operating_unit_sales_id

    
    sales_referral_user_id = fields.Many2one('res.users', string='Sales Referral User')
    sales_referral_ou_id = fields.Many2one('operating.unit', string='Sales Referral Unit', compute='_compute_sales_referral_ou_id', store=True, readonly=False, index=True)

    
    @api.depends('sales_referral_user_id')
    @api.onchange('sales_referral_user_id')
    def _compute_sales_referral_ou_id(self):
        for record in self:
            record.sales_referral_ou_id = False
            if record.sales_referral_user_id:
                record.sales_referral_ou_id = record.sales_referral_user_id.default_operating_unit_sales_id

            
    customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", default="general", tracking=True)
    customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], default="retail", string="Customer Segment", tracking=True)
    customer_pricelist_ids = fields.Many2many('product.pricelist', 'customer_pricelists_geslead', 'pricelist_id', 'geslead_id', string="Customer Pricelists")

    ## Customer CRM - Business Info
    annual_revenues = fields.Monetary(string="Annual Revenues", help="Annual gross revenue/sales of the entity/person")
    employee_count = fields.Integer("Number of Employees")
    countries_covered = fields.Many2many('res.country', 'countries_covered_geslead', 'country_id', 'geslead_id', string='Countries of Business', help="Countries where the entity conduct business")    
    business_brief = fields.Html("Business Brief", help="Brief about the entity, business model, history, track record, market position, etc..")

    ## Customer CRM - Logistics Requirements
    account_requirements = fields.Html("Account Requirements", help="Service/products requirements, volumes, TEUs, type of goods, value of goods, etc..")
    #annual_teus = fields.Integer("Annual Volume in TEUs")
    #ship_type = fields.Selection([('pallet', 'Pallet'), ('container', 'Container'), ('bulk', 'Bulk'), ('others', 'Others')], string='Main Shipping Type')
    #goods_type = fields.Html("Goods Type")
    #goods_value = fields.Html("Goods Value")
    major_countries = fields.Many2many('res.country', 'countries_destinations_geslead', 'country_id', 'geslead_id', string='Major Origins/Destinations')
    services_needed = fields.Many2many('product.product', 'services_needed_geslead', 'product_id', 'geslead_id', string='Services/Products')
    service_categories_needed = fields.Many2many('product.category', 'service_categories_needed_geslead', 'product_category_id', 'geslead_id', string='Categories', compute='_get_services_needed_categories', store=True, compute_sudo=True, depends=['services_needed'])
    @api.depends('services_needed','services_needed.categ_id')
    def _get_services_needed_categories(self):
        for record in self:
            record.service_categories_needed = [(6,0,record.services_needed.categ_id.ids)]

    operation_brief = fields.Html("Operation Note", help="Brief explaination of the operation requirements of the account")
    


    #### VENDOR FIELDS

    # Vendor VRM Fields
    procurement_user_id = fields.Many2one('res.users', string='Procurement User')
    procurement_ou_id = fields.Many2one('operating.unit', string='Procurement Unit', compute='_compute_procurement_ou_id', store=True, readonly=False, index=True)
    
    @api.depends('procurement_user_id')
    @api.onchange('procurement_user_id')
    def _compute_procurement_ou_id(self):
        for record in self:
            record.procurement_ou_id = False
            if record.procurement_user_id:
                record.procurement_ou_id = record.procurement_user_id.default_operating_unit_procurement_id

    procurement_referral_user_id = fields.Many2one('res.users', string='Procurement Referral User')
    procurement_referral_ou_id = fields.Many2one('operating.unit', string='Procurement Referral Unit', compute='_compute_procurement_ou_id', store=True, readonly=False, index=True)
    
    @api.depends('procurement_referral_user_id')
    @api.onchange('procurement_referral_user_id')
    def _compute_procurement_ou_id(self):
        for record in self:
            record.procurement_ou_id = False
            if record.procurement_referral_user_id:
                record.procurement_referral_ou_id = record.procurement_referral_user_id.default_operating_unit_procurement_id
                
    vendor_class = fields.Selection([('general','General Vendor'),('key','Key Vendor'),('strategic','Strategic Vendor')], string="Vendor Class", default="general", tracking=True)
    vendor_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], default="retail", string="Vendor Segment", tracking=True)
    vendor_currency_ids = fields.Many2many('res.currency', 'currencies_geslead', 'currency_id', 'geslead_id', string="Vendor Currencies", help="This currency will be used, instead of the default one, for purchases from the current partner")


    ## Vendor VRM - Business Info
    vendor_annual_revenues = fields.Monetary(string="Annual Revenues", help="Annual gross revenue/sales of the entity/person")
    vendor_employee_count = fields.Integer("Number of Employees")
    vendor_countries_covered = fields.Many2many('res.country', 'vendor_countries_covered_geslead', 'country_id', 'geslead_id', string='Countries of Business', help="Countries where the entity conduct business")    
    vendor_business_brief = fields.Html("Business Brief", help="Brief about the entity, business model, history, track record, market position, etc..")

    ## Vendor VRM - Logistics Requirements
    vendor_account_offerings = fields.Html("Account Offerings", help="Service/products provided, rates, etc..")
    vendor_major_countries = fields.Many2many('res.country', 'vendor_countries_destinations_geslead', 'country_id', 'geslead_id', string='Major Origins/Destinations')
    services_provided = fields.Many2many('product.product', 'vendor_services_needed_geslead', 'product_id', 'geslead_id', string='Services/Products')
    service_categories_provided = fields.Many2many('product.category', 'service_categories_provided_geslead', 'product_category_id', 'geslead_id', string='Categories', compute='_get_services_provided_categories', store=True, compute_sudo=True, depends=['services_provided'])
    @api.depends('services_needed','services_needed.categ_id')
    def _get_services_provided_categories(self):
        for record in self:
            record.service_categories_provided = [(6,0,record.services_provided.categ_id.ids)]
            
    vendor_operation_brief = fields.Html("Operation Note", help="Brief explaination of the operation requirements of the account")
    


    ####check duplication fields
    same_pa_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID', compute='_compute_same_pa_partner_id', store=False)
    same_pa_company_registry_partner_id = fields.Many2one('res.partner', string='Partner with same Company Registry', compute='_compute_same_pa_partner_id', store=False)
    same_pa_name_partner_id = fields.Many2one('res.partner', string='Partner with same Name', compute='_compute_same_pa_partner_id', store=False)
    same_pa_website_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_email_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_phone_partner_id = fields.Many2one('res.partner', string='Partner with same Phone', compute='_compute_same_pa_partner_id', store=False)
    same_pa_mobile_partner_id = fields.Many2one('res.partner', string='Partner with same Mobile', compute='_compute_same_pa_partner_id', store=False)

    same_pa_vat_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Tax ID', compute='_compute_same_pa_lead_id', store=False)
    same_pa_company_registry_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Company Registry', compute='_compute_same_pa_lead_id', store=False)
    same_pa_name_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Name', compute='_compute_same_pa_lead_id', store=False)
    same_pa_website_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Website', compute='_compute_same_pa_lead_id', store=False)
    same_pa_email_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Website', compute='_compute_same_pa_lead_id', store=False)
    same_pa_phone_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Phone', compute='_compute_same_pa_lead_id', store=False)
    same_pa_mobile_lead_id = fields.Many2one('gescrm.lead', string='Lead with same Mobile', compute='_compute_same_pa_lead_id', store=False)


    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'legal_name','website','email','phone','mobile')
    def _compute_same_pa_lead_id(self):
        for lead in self.sudo():
            lead.same_pa_vat_lead_id = False
            lead.same_pa_company_registry_lead_id = False
            lead.same_pa_name_lead_id = False
            lead.same_pa_website_lead_id = False
            lead.same_pa_email_lead_id = False
            lead.same_pa_phone_lead_id = False
            lead.same_pa_mobile_lead_id = False

        
            # use _origin to deal with onchange()
            lead_id = lead._origin.id
            #active_test = False because if a partner has been deactivated you still want to raise the error,
            #so that you can reactivate it instead of creating a new one, which would loose its history.
            Lead = self.with_context(active_test=False).sudo()
            
            odomain = [
                ('id', '!=', lead_id),
            ]
            if lead.company_id:
                odomain += [('company_id', 'in', [False, lead.company_id.id])]

            # check vat
            domain = odomain + [
                ('vat', '=', lead.vat), 
                ('country_id','=',lead.country_id.id),
            ]
            should_check_vat = lead.vat and len(lead.vat) != 1
            lead.same_pa_vat_lead_id = should_check_vat and Lead.search(domain, limit=1)
            
            # check company_registry
            domain = odomain + [
                ('company_registry', '=', lead.company_registry),
                ('country_id','=',lead.country_id.id),
            ]
            lead.same_pa_company_registry_lead_id = bool(lead.company_registry) and Lead.search(domain, limit=1)

            # check name
            domain = odomain + [
                ('legal_name','ilike',lead.legal_name),
                ('country_id','=',lead.country_id.id),
            ]
            lead.same_pa_name_lead_id = bool(lead.legal_name) and Lead.search(domain, limit=1)

            # check website
            domain = odomain + [
                ('website', '=', lead.website),
            ]
            lead.same_pa_website_lead_id = bool(lead.website) and Lead.search(domain, limit=1)

            # check email
            domain = odomain + [
                ('email', '=', lead.email),
            ]
            lead.same_pa_email_lead_id = bool(lead.email) and Lead.search(domain, limit=1)

            # check phone
            domain = odomain + [
                ('phone', '=', lead.phone),
                ('country_id','=',lead.country_id.id),
            ]
            lead.same_pa_phone_lead_id = bool(lead.phone) and Lead.search(domain, limit=1)

            # check mobile
            domain = odomain + [
                ('mobile', '=', lead.mobile),
                ('country_id','=',lead.country_id.id),
            ]
            lead.same_pa_mobile_lead_id = bool(lead.mobile) and Lead.search(domain, limit=1)


    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'legal_name','website','email','phone','mobile')
    def _compute_same_pa_partner_id(self):
        for partner in self.sudo():
            partner.same_pa_vat_partner_id = False
            partner.same_pa_company_registry_partner_id = False
            partner.same_pa_name_partner_id = False
            partner.same_pa_website_partner_id = False
            partner.same_pa_email_partner_id = False
            partner.same_pa_phone_partner_id = False
            partner.same_pa_mobile_partner_id = False

            Partner = self.with_context(active_test=False).env['res.partner'].sudo()
            
            odomain = [
                ('parent_id','=',False),
            ]
            if partner.company_id:
                odomain += [('company_id', 'in', [False, partner.company_id.id])]

            # check vat
            domain = odomain + [
                ('vat', '=', partner.vat), 
                ('country_id','=',partner.country_id.id),
            ]
            should_check_vat = partner.vat and len(partner.vat) != 1
            partner.same_pa_vat_partner_id = should_check_vat and Partner.search(domain, limit=1)
            
            # check company_registry
            domain = odomain + [
                ('company_registry', '=', partner.company_registry),
                ('country_id','=',partner.country_id.id),
            ]
            partner.same_pa_company_registry_partner_id = bool(partner.company_registry) and Partner.search(domain, limit=1)

            # check name
            domain = odomain + [
                ('name','ilike',partner.legal_name),
                ('country_id','=',partner.country_id.id),
            ]
            partner.same_pa_name_partner_id = bool(partner.legal_name) and Partner.search(domain, limit=1)

            # check website
            domain = odomain + [
                ('website', '=', partner.website),
            ]
            partner.same_pa_website_partner_id = bool(partner.website) and Partner.search(domain, limit=1)

            # check email
            domain = odomain + [
                ('email', '=', partner.email),
            ]
            partner.same_pa_email_partner_id = bool(partner.email) and Partner.search(domain, limit=1)

            # check phone
            domain = odomain + [
                ('phone', '=', partner.phone),
                ('country_id','=',partner.country_id.id),
            ]
            partner.same_pa_phone_partner_id = bool(partner.phone) and Partner.search(domain, limit=1)

            # check mobile
            domain = odomain + [
                ('mobile', '=', partner.mobile),
                ('country_id','=',partner.country_id.id),
            ]
            partner.same_pa_mobile_partner_id = bool(partner.mobile) and Partner.search(domain, limit=1)



    def _clean_website(self, website):
        url = urls.url_parse(website)
        if not url.scheme:
            if not url.netloc:
                url = url.replace(netloc=url.path, path='')
            website = url.replace(scheme='http').to_url()
        return website

    

   

    
    def write(self, vals):
      
        
        if vals.get('website'):
            vals['website'] = self._clean_website(vals['website'])
            
        return super(GESCRMLead, self).write(vals)
