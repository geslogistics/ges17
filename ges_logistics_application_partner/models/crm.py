# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json
from lxml import etree






class Lead(models.Model):
    _inherit = 'crm.lead'

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids", store=False)
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True, store=False)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True, store=False)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True, store=False)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True, store=False)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True, store=False)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True, store=False)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True, store=False)

    current_operating_unit_sales_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_id", string="Sales Unit", store=False)
    current_operating_unit_sales_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_ops_id", string="Sales Ops Unit", store=False)
    current_operating_unit_procurement_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_id", string="Procurement Unit", store=False)
    current_operating_unit_procurement_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_ops_id", string="Procurement Ops Unit", store=False)
    current_operating_unit_finance_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_id", string="Finance Unit", store=False)
    current_operating_unit_finance_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_ops_id", string="Finance Ops Unit", store=False)
    current_operating_unit_hr_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_hr_id", string="HR Unit", store=False)
    current_operating_unit_it_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_it_id", string="IT Unit", store=False)
    current_operating_unit_marketing_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_marketing_id", string="Marketing Unit", store=False)
    current_operating_unit_executive_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_executive_id", string="Executive Unit", store=False)

    @api.depends("current_user_id", "current_operating_unit_ids")
    def _compute_current_operating_unit_ids(self):
        for user in self:
            user.current_operating_unit_sales_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales')
            user.current_operating_unit_sales_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')
            user.current_operating_unit_procurement_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement')
            user.current_operating_unit_procurement_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')
            user.current_operating_unit_finance_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance')
            user.current_operating_unit_finance_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')
            user.current_operating_unit_hr_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'hr')
            user.current_operating_unit_it_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'it')
            user.current_operating_unit_executive_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'executive')
            user.current_operating_unit_virtual_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'virtual')
            
    
    
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, readonly=True,
                                  default=lambda self: self.env.company.currency_id.id)

    #### KYC FIELDS
    company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], default="company")
    name_alt_lang = fields.Char(string='Name (AR)', help="Official / Legal Name (AR)")
    trade_name = fields.Char(string='Trading Name', translate=True, help="if different from Legal Entity Name")
    trade_name_alt_lang = fields.Char(string='Trading Name (AR)', translate=True, help="if different from Legal Entity Name")
    company_registry = fields.Char(string="CR/ID Number", help="The official registry/ID number. Use it if it is different from the Tax ID. It must be unique across all partners of a same country")
    company_registry_expiry_date = fields.Date(string="CR/ID Expiry")
    vat = fields.Char(string='Tax ID', help="i.e. VAT Number")
    ref = fields.Char(string='Reference', help="Internal reference to be used for the account")
    legal_type = fields.Selection([('establishment','Establishment'),('joint_liability','Joint Liability Company'),('limited_partnership','Limited Partnership Company'),('simple_joint','Simple Joint Stock Company'),('closed_joint','Closed Joint Stock Company'),('public','Public Joint Stock Company'),('llc','Limited Liability Company'),('one_llc','One Person Limited Liability Company')])
    industry_id = fields.Many2one('res.partner.industry', 'Industry')
    paidup_capital = fields.Monetary("Paid-up Capital", help="As per registration")
    ownership_structure = fields.Html("Ownership Structure", help="List of owners and their ownership percentages")
    management_structure = fields.Html("Management Structure", help="List of account's management team members")
    year_founded = fields.Char("Year Founded")
    country_code = fields.Char(string="Country Code", related='country_id.code')
    l10n_sa_edi_building_number = fields.Char("Building Number")
    l10n_sa_edi_plot_identification = fields.Char("Plot Identification")
    city_id = fields.Many2one(comodel_name='res.city', string='City')
    country_enforce_cities = fields.Boolean(related='country_id.enforce_cities')

    contact_partner_id = fields.Many2one('res.partner', string="Contact Person", domain="[('parent_id','=',partner_id)]")

    #### CRM Fields

    # Customer CRM Fields
    customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", default="general", tracking=True)
    customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], default="retail", string="Customer Segment", tracking=True)
    customer_pricelist_ids = fields.Many2many('product.pricelist', 'customer_pricelists_lead', 'pricelist_id', 'lead_id', string="Customer Pricelists")
    deal_min_margin = fields.Float(string="Deal Min. Margin %", help="Specify a minimum target bundle margin per deal/order", default=0)

    ## Customer CRM - Business Info
    annual_revenues = fields.Monetary(string="Annual Revenues", help="Annual gross revenue/sales of the entity/person")
    employee_count = fields.Integer("Number of Employees")
    countries_covered = fields.Many2many('res.country', 'countries_covered_lead', 'country_id', 'lead_id', string='Countries of Business', help="Countries where the entity conduct business")    
    business_brief = fields.Html("Business Brief", help="Brief about the entity, business model, history, track record, market position, etc..")

    ## Customer CRM - Logistics Requirements
    account_requirements = fields.Html("Account Requirements", help="Service/products requirements, volumes, TEUs, type of goods, value of goods, etc..")
    major_countries = fields.Many2many('res.country', 'countries_destinations_lead', 'country_id', 'lead_id', string='Major Origins/Destinations')
    services_needed = fields.Many2many('product.product', 'services_needed_lead', 'product_id', 'lead_id', string='Services/Products')
    service_categories_needed = fields.Many2many('product.category', 'service_categories_needed_lead', 'product_id', 'lead_id', string='Categories', compute='_get_services_categories', store=True, compute_sudo=True, depends=['services_needed'])
    operation_brief = fields.Html("Operation Note", help="Brief explaination of the operation requirements of the account")

    @api.depends('services_needed','services_needed.categ_id')
    def _get_services_categories(self):
        for record in self:
            record.service_categories_needed = [(6,0,record.services_needed.categ_id.ids)]

    #### Customer Credit Fields
    monthly_expected_business = fields.Monetary(string="Monthly Expected Sales", help="Expected monthly account revenues")
    customer_credit_limit = fields.Monetary(string="Customer Credit Limit")
    credit_trade_references = fields.Html(string="Trade References", help="Please provide at least 3 Credit Trade References")
    #customer_payment_term_ids = fields.Many2many('account.payment.term', 'customer_payment_terms_lead', 'term_id', 'lead_id', string="Customer Payment Terms")
    customer_payment_term_ids = fields.Many2one('account.payment.term', string="Customer Payment Terms")


    #### PARTNER RELATED PA FIELDS

    #### PARTNER RELATED ORIGINAL FIELDS
    pa_sales_user_id = fields.Many2one('res.users', string='Sales User', store=True, related="partner_id.sales_user_id")
    pa_sales_ou_id = fields.Many2one('operating.unit', string='Sales Unit', related="partner_id.sales_ou_id")
    pa_street = fields.Char(store=True, related="partner_id.street")
    pa_street2 = fields.Char(store=True, related="partner_id.street2")
    pa_zip = fields.Char(store=True, related="partner_id.zip")
    pa_city = fields.Char(store=True, related="partner_id.city")
    pa_city_id = fields.Many2one(comodel_name='res.city', string='City ID', related="partner_id.city_id")
    pa_country_enforce_cities = fields.Boolean(related='pa_country_id.enforce_cities')
    pa_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', store=True, related="partner_id.state_id")
    pa_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', store=True, related="partner_id.country_id")
    pa_country_code = fields.Char(string="Country Code", related='pa_country_id.code')
    pa_l10n_sa_edi_building_number = fields.Char("Building Number", related="partner_id.l10n_sa_edi_building_number")
    pa_l10n_sa_edi_plot_identification = fields.Char("Plot Identification", related="partner_id.l10n_sa_edi_plot_identification")

    pa_email = fields.Char(store=True, related="contact_partner_id.email")
    pa_email_cc = fields.Char(store=True, related="email_cc")
    pa_phone = fields.Char(store=True, related="partner_id.phone")
    pa_mobile = fields.Char(store=True, related="contact_partner_id.mobile")
    pa_website = fields.Char('Website Link', store=True, related="partner_id.website")

    pa_contact_name = fields.Char("Contact Name", store=True, related="contact_partner_id.name")
    pa_function = fields.Char("Job Position", store=True, related="contact_partner_id.function")
    pa_title = fields.Many2one('res.partner.title', string="Title", store=True, related="contact_partner_id.title")

    #### PARTNER RELATED KYC FIELDS
    pa_company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], store=True, related="partner_id.company_type")
    pa_name_alt_lang = fields.Char(string='Name (AR)', store=True, related="partner_id.current_kyc_id.name_alt_lang")
    pa_trade_name = fields.Char(string='Trading Name', store=True, related="partner_id.current_kyc_id.trade_name")
    pa_trade_name_alt_lang = fields.Char(string='Trading Name (AR)', store=True, related="partner_id.current_kyc_id.trade_name_alt_lang")
    pa_company_registry = fields.Char(string="CR/ID Number", store=True, related="partner_id.company_registry")
    pa_company_registry_expiry_date = fields.Date(string="CR/ID Expiry", store=True, related="partner_id.current_kyc_id.company_registry_expiry_date")
    pa_vat = fields.Char(string='Tax ID', store=True, related="partner_id.vat")
    pa_ref = fields.Char(string='Reference', store=True, related="partner_id.ref")
    pa_legal_type = fields.Selection([('establishment','Establishment'),('joint_liability','Joint Liability Company'),('limited_partnership','Limited Partnership Company'),('simple_joint','Simple Joint Stock Company'),('closed_joint','Closed Joint Stock Company'),('public','Public Joint Stock Company'),('llc','Limited Liability Company'),('one_llc','One Person Limited Liability Company')], store=True, related="partner_id.current_kyc_id.legal_type")
    pa_industry_id = fields.Many2one('res.partner.industry', 'Industry', store=True, related="partner_id.industry_id")
    pa_paidup_capital = fields.Monetary("Paid-up Capital", store=True, related="partner_id.current_kyc_id.paidup_capital")
    pa_ownership_structure = fields.Html("Ownership Structure", store=True, related="partner_id.current_kyc_id.ownership_structure")
    pa_management_structure = fields.Html("Management Structure", store=True, related="partner_id.current_kyc_id.management_structure")
    pa_year_founded = fields.Char("Year Founded", store=True, related="partner_id.current_kyc_id.year_founded")

    #### PARTNER RELATED CRM Fields

    # PARTNER RELATED Customer CRM Fields
    pa_customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", store=True, related="partner_id.current_crm_id.customer_class")
    pa_customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], string="Customer Segment", store=True, related="partner_id.current_crm_id.customer_segment")
    pa_customer_pricelist_ids = fields.Many2many('product.pricelist', 'customer_pa_pricelists_lead', 'pa_pricelist_id', 'pa_lead_id', string="Customer Pricelists", store=True, related="partner_id.current_crm_id.customer_pricelist_ids")
    pa_deal_min_margin = fields.Float(string="Deal Min. Margin %", related="partner_id.current_crm_id.deal_min_margin")

    ## PARTNER RELATED Customer CRM - Business Info
    pa_annual_revenues = fields.Monetary(string="Annual Revenues", store=True, related="partner_id.current_crm_id.annual_revenues")
    pa_employee_count = fields.Integer("Number of Employees", store=True, related="partner_id.current_crm_id.employee_count")
    pa_countries_covered = fields.Many2many('res.country', 'countries_pa_covered_lead', 'pa_country_id', 'pa_lead_id', string='Countries of Business', store=True, related="partner_id.current_crm_id.countries_covered")
    pa_business_brief = fields.Html("Business Brief", store=True, related="partner_id.current_crm_id.business_brief")

    ## PARTNER RELATED Customer CRM - Logistics Requirements
    pa_account_requirements = fields.Html("Account Requirements", store=True, related="partner_id.current_crm_id.account_requirements")
    pa_major_countries = fields.Many2many('res.country', 'countries_destinations_lead', 'country_id', 'lead_id', string='Major Origins/Destinations', store=True, related="partner_id.current_crm_id.major_countries")
    pa_services_needed = fields.Many2many('product.product', 'services_needed_lead', 'product_id', 'lead_id', string='Services/Products', store=True, related="partner_id.current_crm_id.services_needed")
    pa_service_categories_needed = fields.Many2many('product.category', 'service_categories_needed_lead', 'product_id', 'lead_id', string='Categories', store=True, related="partner_id.current_crm_id.service_categories_needed")
    pa_operation_brief = fields.Html("Operation Note", store=True, related="partner_id.current_crm_id.operation_brief")
    
    #### PARTNER RELATED Customer Credit Fields
    pa_monthly_expected_business = fields.Monetary(string="Monthly Expected Sales", related="partner_id.current_customer_credit_id.monthly_expected_business")
    pa_customer_credit_limit = fields.Monetary(string="Customer Credit Limit", related="partner_id.current_customer_credit_id.customer_credit_limit")
    pa_credit_trade_references = fields.Html(string="Trade References", related="partner_id.current_customer_credit_id.credit_trade_references")
    #pa_customer_payment_term_ids = fields.Many2many('account.payment.term', 'customer_pa_payment_terms_lead', 'pa_term_id', 'pa_lead_id', string="Customer Payment Terms", related="partner_id.current_customer_credit_id.customer_payment_term_ids")
    pa_customer_payment_term_ids = fields.Many2one('account.payment.term', string="Customer Payment Terms", related="partner_id.current_customer_credit_id.customer_payment_term_ids")

    
    
    

    ####check duplication fields
    same_pa_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID', compute='_compute_same_pa_partner_id', store=False)
    same_pa_company_registry_partner_id = fields.Many2one('res.partner', string='Partner with same Company Registry', compute='_compute_same_pa_partner_id', store=False)
    same_pa_name_partner_id = fields.Many2one('res.partner', string='Partner with same Name', compute='_compute_same_pa_partner_id', store=False)
    same_pa_website_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_email_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_phone_partner_id = fields.Many2one('res.partner', string='Partner with same Phone', compute='_compute_same_pa_partner_id', store=False)
    same_pa_mobile_partner_id = fields.Many2one('res.partner', string='Partner with same Mobile', compute='_compute_same_pa_partner_id', store=False)

    same_pa_vat_lead_id = fields.Many2one('crm.lead', string='Lead with same Tax ID', compute='_compute_same_pa_lead_id', store=False)
    same_pa_company_registry_lead_id = fields.Many2one('crm.lead', string='Lead with same Company Registry', compute='_compute_same_pa_lead_id', store=False)
    same_pa_name_lead_id = fields.Many2one('crm.lead', string='Lead with same Name', compute='_compute_same_pa_lead_id', store=False)
    same_pa_website_lead_id = fields.Many2one('crm.lead', string='Lead with same Website', compute='_compute_same_pa_lead_id', store=False)
    same_pa_email_lead_id = fields.Many2one('crm.lead', string='Lead with same Website', compute='_compute_same_pa_lead_id', store=False)
    same_pa_phone_lead_id = fields.Many2one('crm.lead', string='Lead with same Phone', compute='_compute_same_pa_lead_id', store=False)
    same_pa_mobile_lead_id = fields.Many2one('crm.lead', string='Lead with same Mobile', compute='_compute_same_pa_lead_id', store=False)

    
    ## stage pa checklist fields
    requires_kyc = fields.Boolean(string="KYC", related="stage_id.requires_kyc")
    requires_crm = fields.Boolean(string="CRM", related="stage_id.requires_crm")
    requires_cc = fields.Boolean(string="CC", related="stage_id.requires_cc")
    requires_cs = fields.Boolean(string="CS", related="stage_id.requires_cs")
    requires_vrm = fields.Boolean(string="VRM", related="stage_id.requires_vrm")
    requires_vc = fields.Boolean(string="VC", related="stage_id.requires_vc")
    requires_vs = fields.Boolean(string="VS", related="stage_id.requires_vs")

    @api.onchange('pa_city_id')
    def _onchange_pa_city_id(self):
        if self.pa_city_id:
            self.pa_city = self.pa_city_id.name
            self.pa_zip = self.pa_city_id.zipcode
            self.pa_state_id = self.pa_city_id.state_id
        elif self._origin:
            self.pa_city = False
            self.pa_zip = False
            self.pa_state_id = False

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

    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'partner_name','website','email_from','phone','mobile')
    #@api.onchange('vat', 'company_id', 'company_registry')
    def _compute_same_pa_partner_id(self):
        for partner in self.sudo():
            if partner.type != 'lead':
                partner.same_pa_vat_partner_id = False
                partner.same_pa_company_registry_partner_id = False
                partner.same_pa_name_partner_id = False
                partner.same_pa_website_partner_id = False
                partner.same_pa_email_partner_id = False
                partner.same_pa_phone_partner_id = False
                partner.same_pa_mobile_partner_id = False

            if partner.type == 'lead':
                # use _origin to deal with onchange()
                partner_id = partner.partner_id._origin.id
                #active_test = False because if a partner has been deactivated you still want to raise the error,
                #so that you can reactivate it instead of creating a new one, which would loose its history.
                Partner = self.with_context(active_test=False).env['res.partner'].sudo()
                
                # check vat
                domain = [
                    ('vat', '=', partner.vat),
                    ('country_id','=',partner.country_id.id),
                    #('duplicate_approved', '=', False), 
                ]
                if partner.company_id:
                    domain += [('company_id', 'in', [False, partner.company_id.id])]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]

                # For VAT number being only one character, we will skip the check just like the regular check_vat
                should_check_vat = partner.vat and len(partner.vat) != 1
                partner.same_pa_vat_partner_id = should_check_vat and Partner.search(domain, limit=1)
                
                # check company_registry
                domain = [
                    ('company_registry', '=', partner.company_registry),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_company_registry_partner_id = bool(partner.company_registry) and Partner.search(domain, limit=1)

                # check name
                domain = [
                    ('name', 'ilike', partner.partner_name),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_name_partner_id = bool(partner.partner_name) and Partner.search(domain, limit=1)

                # check website
                domain = [
                    ('website', '=', partner.website),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_website_partner_id = bool(partner.website) and Partner.search(domain, limit=1)

                # check email
                domain = [
                    ('email', '=', partner.email_from),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_email_partner_id = bool(partner.email_from) and Partner.search(domain, limit=1)

                # check phone
                domain = [
                    ('phone', '=', partner.phone),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_phone_partner_id = bool(partner.phone) and Partner.search(domain, limit=1)

                # check mobile
                domain = [
                    ('mobile', '=', partner.mobile),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                partner.same_pa_mobile_partner_id = bool(partner.mobile) and Partner.search(domain, limit=1)

    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'partner_name','website','email_from','phone','mobile')
    #@api.onchange('vat', 'company_id', 'company_registry')
    def _compute_same_pa_lead_id(self):
        for lead in self.sudo():
            lead.same_pa_vat_lead_id = False
            lead.same_pa_company_registry_lead_id = False
            lead.same_pa_name_lead_id = False
            lead.same_pa_website_lead_id = False
            lead.same_pa_email_lead_id = False
            lead.same_pa_phone_lead_id = False
            lead.same_pa_mobile_lead_id = False

            if lead.type == 'lead' and not lead.partner_id.duplicate_approved:
                # use _origin to deal with onchange()
                lead_id = lead._origin.id
                #active_test = False because if a partner has been deactivated you still want to raise the error,
                #so that you can reactivate it instead of creating a new one, which would loose its history.
                Lead = self.with_context(active_test=False).sudo()
                
                # check vat
                domain = [
                    ('type','=','lead'),
                    ('vat', '=', lead.vat), 
                    ('country_id','=',lead.country_id.id),
                ]
                if lead.company_id:
                    domain += [('company_id', 'in', [False, lead.company_id.id])]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                # For VAT number being only one character, we will skip the check just like the regular check_vat
                should_check_vat = lead.vat and len(lead.vat) != 1
                lead.same_pa_vat_lead_id = should_check_vat and Lead.search(domain, limit=1)
                
                # check company_registry
                domain = [
                    ('type','=','lead'),
                    ('company_registry', '=', lead.company_registry),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                lead.same_pa_company_registry_lead_id = bool(lead.company_registry) and Lead.search(domain, limit=1)

                # check name
                domain = [
                    ('type','=','lead'),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                domain += ['|','&',('type','=','lead'),('partner_name', 'ilike', lead.partner_name),'&',('type','!=','lead'),('partner_id.name', 'ilike', lead.partner_name)]
                lead.same_pa_name_lead_id = bool(lead.partner_name) and Lead.search(domain, limit=1)

                # check website
                domain = [
                    ('type','=','lead'),
                    ('website', '=', lead.website),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                lead.same_pa_website_lead_id = bool(lead.website) and Lead.search(domain, limit=1)

                # check email
                domain = [
                    ('type','=','lead'),
                    ('email_from', '=', lead.email_from),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                lead.same_pa_email_lead_id = bool(lead.email_from) and Lead.search(domain, limit=1)

                # check phone
                domain = [
                    ('type','=','lead'),
                    ('phone', '=', lead.phone),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                lead.same_pa_phone_lead_id = bool(lead.phone) and Lead.search(domain, limit=1)

                # check mobile
                domain = [
                    ('type','=','lead'),
                    ('mobile', '=', lead.mobile),
                    ('country_id','=',lead.country_id.id),
                    ('company_id', 'in', [False, lead.company_id.id]),
                ]
                if lead_id:
                    domain += [('id', '!=', lead_id)]
                if lead.partner_id.parent_id:
                    domain += [('id', '!=', lead.partner_id.parent_id.id)]
                lead.same_pa_mobile_lead_id = bool(lead.mobile) and Lead.search(domain, limit=1)


    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        #execute original
        res2 = super(Lead, self)._prepare_customer_values(partner_name, is_company, parent_id)

        #add values (override)
        res2['l10n_sa_edi_building_number'] = self.l10n_sa_edi_building_number
        res2['l10n_sa_edi_plot_identification'] = self.l10n_sa_edi_plot_identification
        res2['company_registry'] = self.company_registry
        res2['vat'] = self.vat
        res2['ref'] = self.ref
        res2['function'] = self.function if not is_company else False
        res2['title'] = self.title.id if not is_company else False
        return res2

    
    def _create_customer(self):
        #raise UserError('test')
        #original code
        """ Create a partner from lead data and link it to the lead.

        :return: newly-created partner browse record
        """
        Partner = self.env['res.partner']
        contact_name = self.contact_name
        if not contact_name:
            contact_name = parse_contact_from_email(self.email_from)[0] if self.email_from else False

        if self.partner_name:
            partner_company = Partner.create(self._prepare_customer_values(self.partner_name, is_company=True))
        elif self.partner_id:
            partner_company = self.partner_id
        else:
            partner_company = None
        
        #override method
        
        if self.contact_name:
            person_contact = Partner.create(self._prepare_customer_values(contact_name, is_company=False, parent_id=partner_company.id if partner_company else False))
        elif self.contact_partner_id:
            person_contact = self.contact_partner_id
        else:
            person_contact = None

        self.contact_partner_id = person_contact
        
        
        if self.company_type == 'person':
            return person_contact
        elif self.company_type == 'company':
            return partner_company
        #end of override
        


        return Partner.create(self._prepare_customer_values(self.name, is_company=False))

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_contact_partner_id(self):
        self.contact_partner_id = False
    
    @api.depends('company_type','partner_name','contact_name','partner_id')
    @api.onchange('company_type','partner_name','contact_name','partner_id')
    def _update_record_name_pa_lead(self):
        
        if self.company_type == 'person':
            self.partner_name = False
            if self.contact_name and not self.name:
                self.name = self.contact_name
                
            
        if self.company_type == 'company':
            if self.contact_name and self.partner_name:
                if self.contact_name == self.partner_name:
                    raise UserError("For companies, the Contact Name must be the name of the actual contact person within the company (and different from the Name of the company).")
                    
            if self.partner_name and not self.name:
                self.name = self.partner_name
        
                
    # current application fields
    #Application fields
    current_kyc_id = fields.Many2one('application.partner', string="KYC Application", related="partner_id.current_kyc_id")
    current_kyc_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='KYC Status', related="current_kyc_id.state")
    current_kyc_expiry_date = fields.Date(string="KYC Expiry Date", related="current_kyc_id.expiry_date")
    current_kyc_review_date = fields.Date(string="KYC Review Date", related="current_kyc_id.review_date")

    current_crm_id = fields.Many2one('application.partner', string="CRM Application", related="partner_id.current_crm_id")
    current_crm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='CRM Status', related="current_crm_id.state")
    current_crm_expiry_date = fields.Date(string="CRM Expiry Date", related="current_crm_id.expiry_date")
    current_crm_review_date = fields.Date(string="CRM Review Date", related="current_crm_id.review_date")

    current_vrm_id = fields.Many2one('application.partner', string="VRM Application", related="partner_id.current_vrm_id")
    current_vrm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='VRM Status', related="current_vrm_id.state")
    current_vrm_expiry_date = fields.Date(string="VRM Expiry Date", related="current_vrm_id.expiry_date")
    current_vrm_review_date = fields.Date(string="VRM Review Date", related="current_vrm_id.review_date")

    current_customer_credit_id = fields.Many2one('application.partner', string="Customer Credit Application", related="partner_id.current_customer_credit_id")
    current_customer_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Credit Status', related="current_customer_credit_id.state")
    current_customer_credit_expiry_date = fields.Date(string="Customer Credit Expiry Date", related="current_customer_credit_id.expiry_date")
    current_customer_credit_review_date = fields.Date(string="Customer Credit Review Date", related="current_customer_credit_id.review_date")

    current_vendor_credit_id = fields.Many2one('application.partner', string="Vendor Credit Application", related="partner_id.current_vendor_credit_id")
    current_vendor_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Credit Status', related="current_vendor_credit_id.state")
    current_vendor_credit_expiry_date = fields.Date(string="Vendor Credit Expiry Date", related="current_vendor_credit_id.expiry_date")
    current_vendor_credit_review_date = fields.Date(string="Vendor Credit Review Date", related="current_vendor_credit_id.review_date")

    current_customer_strategy_id = fields.Many2one('application.partner', string="Customer Strategy Credit Application", related="partner_id.current_customer_strategy_id")
    current_customer_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Strategy Status', related="current_customer_strategy_id.state")
    current_customer_strategy_expiry_date = fields.Date(string="Customer Strategy Expiry Date", related="current_customer_strategy_id.expiry_date")
    current_customer_strategy_review_date = fields.Date(string="Customer Strategy Review Date", related="current_customer_strategy_id.review_date")
    
    current_vendor_strategy_id = fields.Many2one('application.partner', string="Vendor Strategy Credit Application", related="partner_id.current_vendor_strategy_id")
    current_vendor_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Strategy Status', related="current_vendor_strategy_id.state")
    current_vendor_strategy_expiry_date = fields.Date(string="Vendor Strategy Expiry Date", related="current_vendor_strategy_id.expiry_date")
    current_vendor_strategy_review_date = fields.Date(string="Vendor Strategy Review Date", related="current_vendor_strategy_id.review_date")

   
    def initiate_partner_application(self): 
        return self.partner_id.initiate_partner_application()
        


    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        hide_list = [
            'account_requirements',
            'annual_revenues',
            'name_alt_lang',
            'business_brief',
            'company_registry',
            'company_registry_expiry_date',
            'company_type',
            'contact_partner_id',
            'country_code',
            'countries_covered',
            'credit_trade_references',
            'currency_id',
            'current_crm_expiry_date',
            'current_crm_id',
            'current_crm_review_date',
            'current_crm_state',
            'current_customer_credit_expiry_date',
            'current_customer_credit_id',
            'current_customer_credit_review_date',
            'current_customer_credit_state',
            'current_customer_strategy_expiry_date',
            'current_customer_strategy_id',
            'current_customer_strategy_review_date',
            'current_customer_strategy_state',
            'current_kyc_expiry_date',
            'current_kyc_id',
            'current_kyc_review_date',
            'current_kyc_state',
            'current_user_id',
            'current_user_id',
            'current_vendor_credit_expiry_date',
            'current_vendor_credit_id',
            'current_vendor_credit_review_date',
            'current_vendor_credit_state',
            'current_vendor_strategy_expiry_date',
            'current_vendor_strategy_id',
            'current_vendor_strategy_review_date',
            'current_vendor_strategy_state',
            'current_vrm_expiry_date',
            'current_vrm_id',
            'current_vrm_review_date',
            'current_vrm_state',
            'customer_class',
            'customer_credit_limit',
            'customer_payment_term_ids',
            'customer_pricelist_ids',
            'deal_min_margin',
            'customer_segment',
            'employee_count',
            'industry_id',
            'legal_type',
            'major_countries',
            'management_structure',
            'monthly_expected_business',
            'operation_brief',
            'ownership_structure',
            'pa_account_requirements',
            'pa_annual_revenues',
            'pa_name_alt_lang',
            'pa_business_brief',
            'pa_city',
            'pa_city_id',
            'pa_company_registry',
            'pa_company_registry_expiry_date',
            'pa_company_type',
            'pa_contact_name',
            'pa_countries_covered',
            'pa_country_id',
            'pa_country_code',
            'pa_l10n_sa_edi_building_number',
            'pa_l10n_sa_edi_plot_identification',
            #'l10n_sa_edi_building_number',
            #'l10n_sa_edi_plot_identification',
            'pa_credit_trade_references',
            'pa_customer_class',
            'pa_customer_credit_limit',
            'pa_customer_payment_term_ids',
            'pa_customer_pricelist_ids',
            'pa_deal_min_margin',
            'pa_customer_segment',
            'pa_email',
            'pa_email_cc',
            'pa_employee_count',
            'pa_function',
            'pa_industry_id',
            'pa_legal_type',
            'pa_major_countries',
            'pa_management_structure',
            'pa_mobile',
            'pa_monthly_expected_business',
            'pa_operation_brief',
            'pa_ownership_structure',
            'pa_paidup_capital',
            'pa_phone',
            'pa_ref',
            'pa_service_categories_needed',
            'pa_services_needed',
            'pa_state_id',
            'pa_street',
            'pa_street2',
            'pa_team_id',
            'pa_title',
            'pa_trade_name',
            'pa_trade_name_alt_lang',
            'pa_user_id',
            'pa_vat',
            'pa_website',
            'pa_year_founded',
            'pa_zip',
            'paidup_capital',
            'ref',
            'same_pa_company_registry_lead_id',
            'same_pa_company_registry_partner_id',
            'same_pa_email_lead_id',
            'same_pa_email_partner_id',
            'same_pa_mobile_lead_id',
            'same_pa_mobile_partner_id',
            'same_pa_name_lead_id',
            'same_pa_name_partner_id',
            'same_pa_phone_lead_id',
            'same_pa_phone_partner_id',
            'same_pa_vat_lead_id',
            'same_pa_vat_partner_id',
            'same_pa_website_lead_id',
            'same_pa_website_partner_id',
            'service_categories_needed',
            'services_needed',
            'trade_name',
            'trade_name_alt_lang',
            'vat',
            'year_founded',
        ]
        for field in hide_list:
            if res.get(field):
                res[field]['searchable'] = False
                res[field]['selectable'] = False # to hide in Add Custom filter view
                res[field]['sortable'] = False # to hide in group by view
                res[field]['exportable'] = False # to hide in export list
                res[field]['store'] = False # to hide in 'Select Columns' filter in tree views

        return res

    def create(self, values):
        #check VAT
        if (values.get('pa_vat') or self.pa_vat) and (values.get('pa_country_id') or self.pa_country_id):
            vat = values.get('pa_vat') or self.pa_vat
            country = self.env['res.country'].search([('id','=',values.get('pa_country_id'))]) or self.pa_country_id
            if self.partner_id._run_vat_test(vat,country) is False:
                raise UserError("Tax ID / VAT Number - Format Error")
        
        return super(Lead, self).create(values)

    def write(self, values):

        #check stage requirements
        if values.get("stage_id"):
            new_stage_id = self.env["crm.stage"].browse(values.get("stage_id"))
            if new_stage_id.requires_kyc and not self.partner_id.current_kyc_state == 'active':
                raise UserError("KYC is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_crm and not self.partner_id.current_crm_state == 'active':
                raise UserError("CRM is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_cc and not self.partner_id.current_customer_credit_state == 'active':
                raise UserError("CC is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_cs and not self.partner_id.current_customer_strategy_state == 'active':
                raise UserError("CS is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_vrm and not self.partner_id.current_vrm_state == 'active':
                raise UserError("VRM is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_vc and not self.partner_id.current_vendor_credit_state == 'active':
                raise UserError("VC is required for " + new_stage_id.name + " stage.")
            if new_stage_id.requires_vs and not self.partner_id.current_vendor_strategy_state == 'active':
                raise UserError("VS is required for " + new_stage_id.name + " stage.")

        #check VAT
        if (values.get('pa_vat') or self.pa_vat) and (values.get('pa_country_id') or self.pa_country_id):
            vat = values.get('pa_vat') or self.pa_vat
            country = self.env['res.country'].search([('id','=',values.get('pa_country_id'))]) or self.pa_country_id
            if self.partner_id._run_vat_test(vat,country) is False:
                raise UserError("Tax ID / VAT Number - Format Error")
        
        return super(Lead, self).write(values)

class Lead2OpportunityPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids", store=False)
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True, store=False)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True, store=False)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True, store=False)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True, store=False)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True, store=False)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True, store=False)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True, store=False)

    current_operating_unit_sales_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_id", string="Sales Unit", store=False)
    current_operating_unit_sales_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_ops_id", string="Sales Ops Unit", store=False)
    current_operating_unit_procurement_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_id", string="Procurement Unit", store=False)
    current_operating_unit_procurement_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_ops_id", string="Procurement Ops Unit", store=False)
    current_operating_unit_finance_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_id", string="Finance Unit", store=False)
    current_operating_unit_finance_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_ops_id", string="Finance Ops Unit", store=False)
    current_operating_unit_hr_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_hr_id", string="HR Unit", store=False)
    current_operating_unit_it_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_it_id", string="IT Unit", store=False)
    current_operating_unit_marketing_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_marketing_id", string="Marketing Unit", store=False)
    current_operating_unit_executive_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_executive_id", string="Executive Unit", store=False)

    @api.depends("current_user_id", "current_operating_unit_ids")
    def _compute_current_operating_unit_ids(self):
        for user in self:
            user.current_operating_unit_sales_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales')
            user.current_operating_unit_sales_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')
            user.current_operating_unit_procurement_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement')
            user.current_operating_unit_procurement_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')
            user.current_operating_unit_finance_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance')
            user.current_operating_unit_finance_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')
            user.current_operating_unit_hr_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'hr')
            user.current_operating_unit_it_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'it')
            user.current_operating_unit_executive_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'executive')
            user.current_operating_unit_virtual_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'virtual')
            
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.action = 'create'
        self.name = 'convert'


class Stage(models.Model):

    _inherit = "crm.stage"

    requires_kyc = fields.Boolean(string="KYC")
    requires_crm = fields.Boolean(string="CRM")
    requires_cc = fields.Boolean(string="CC")
    requires_cs = fields.Boolean(string="CS")
    requires_vrm = fields.Boolean(string="VRM")
    requires_vc = fields.Boolean(string="VC")
    requires_vs = fields.Boolean(string="VS")
