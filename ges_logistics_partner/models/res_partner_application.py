# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from pytz import timezone

class ResPartnerApplication(models.Model):
    _name = 'res.partner.application'
    _description = "Partner Applications"
    _order = 'create_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    color = fields.Integer('Color')

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True,
                                  string='Currency')

    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('validated', 'Validated'), ('approved', 'Approved'), ('rejected', 'Rejected'),('active', 'Active'),('expired', 'Expired'),('cancel', 'Cancelled')], default='draft', string='Status')
    
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    current_sale_team_id = fields.Many2one('crm.team', string='Sales Team', related="current_user_id.sale_team_id")
    current_purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team', related="current_user_id.purchase_team_id")

    def _domain_partner_id(self):
        if self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs'):
            return "[(1, '=', 1)]"

        if self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs'):
            return "['|','|','|','&',('team_id', '=', current_sale_team_id),('team_id', '!=', False),'&',('purchase_partner_team_id', '=', current_purchase_team_id),('purchase_partner_team_id', '!=', False),'&',('user_id', '=', current_user_id),('user_id', '!=', False),'&',('buyer_id', '=', current_user_id),('buyer_id', '!=', False)]"

        return "['|',('user_id', '=', current_user_id),('buyer_id', '=', current_user_id)]"
            
    partner_id = fields.Many2one("res.partner", string="Partner", domain=lambda self: self._domain_partner_id())

    is_late_review = fields.Boolean(string="Late Review", default=False)

    is_admin = fields.Boolean(compute='_check_admin_group')

    def _check_admin_group(self):
        if self.user_has_groups('ges_logistics_partner.group_partner_application_admin'):
            self.is_admin = True
        else:
            self.is_admin = False
    

    # current application fields
    #Application fields
    current_kyc_id = fields.Many2one('res.partner.application', string="KYC Application", tracking=True, compute="_get_current_applications", store=True)
    current_kyc_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='KYC Status', related="current_kyc_id.state")
    current_kyc_expiry_date = fields.Date(string="KYC Expiry Date", related="current_kyc_id.expiry_date")
    current_kyc_review_date = fields.Date(string="KYC Review Date", related="current_kyc_id.review_date")

    current_crm_id = fields.Many2one('res.partner.application', string="CRM Application", tracking=True, compute="_get_current_applications", store=True)
    current_crm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='CRM Status', related="current_crm_id.state")
    current_crm_expiry_date = fields.Date(string="CRM Expiry Date", related="current_crm_id.expiry_date")
    current_crm_review_date = fields.Date(string="CRM Review Date", related="current_crm_id.review_date")

    current_vrm_id = fields.Many2one('res.partner.application', string="VRM Application", tracking=True, compute="_get_current_applications", store=True)
    current_vrm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='VRM Status', related="current_vrm_id.state")
    current_vrm_expiry_date = fields.Date(string="VRM Expiry Date", related="current_vrm_id.expiry_date")
    current_vrm_review_date = fields.Date(string="VRM Review Date", related="current_vrm_id.review_date")

    current_customer_credit_id = fields.Many2one('res.partner.application', string="Customer Credit Application", tracking=True, compute="_get_current_applications", store=True)
    current_customer_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Credit Status', related="current_customer_credit_id.state")
    current_customer_credit_expiry_date = fields.Date(string="Customer Credit Expiry Date", related="current_customer_credit_id.expiry_date")
    current_customer_credit_review_date = fields.Date(string="Customer Credit Review Date", related="current_customer_credit_id.review_date")

    current_vendor_credit_id = fields.Many2one('res.partner.application', string="Vendor Credit Application", tracking=True, compute="_get_current_applications", store=True)
    current_vendor_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Credit Status', related="current_vendor_credit_id.state")
    current_vendor_credit_expiry_date = fields.Date(string="Vendor Credit Expiry Date", related="current_vendor_credit_id.expiry_date")
    current_vendor_credit_review_date = fields.Date(string="Vendor Credit Review Date", related="current_vendor_credit_id.review_date")

    current_customer_strategy_id = fields.Many2one('res.partner.application', string="Customer Strategy Credit Application", tracking=True, compute="_get_current_applications", store=True)
    current_customer_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Strategy Status', related="current_customer_strategy_id.state")
    current_customer_strategy_expiry_date = fields.Date(string="Customer Strategy Expiry Date", related="current_customer_strategy_id.expiry_date")
    current_customer_strategy_review_date = fields.Date(string="Customer Strategy Review Date", related="current_customer_strategy_id.review_date")
    
    current_vendor_strategy_id = fields.Many2one('res.partner.application', string="Vendor Strategy Credit Application", tracking=True, compute="_get_current_applications", store=True)
    current_vendor_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Strategy Status', related="current_vendor_strategy_id.state")
    current_vendor_strategy_expiry_date = fields.Date(string="Vendor Strategy Expiry Date", related="current_vendor_strategy_id.expiry_date")
    current_vendor_strategy_review_date = fields.Date(string="Vendor Strategy Review Date", related="current_vendor_strategy_id.review_date")
    
    #application_direction = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor')], default='customer', string='Direction')
    #is_kyc = fields.Boolean("KYC Application")
    #is_crm = fields.Boolean("CRM Application")
    #is_vrm = fields.Boolean("VRM Application")
    #is_customer_credit = fields.Boolean("Customer Credit")
    #is_vendor_credit = fields.Boolean("Vendor Credit")
    #is_customer_strategy = fields.Boolean("Customer Strategy")
    #is_vendor_strategy = fields.Boolean("Vendor Strategy")
    #application_types = fields.Char(string="Application Type(s)", compute="_get_application_types")
    
    application_type = fields.Selection([('kyc', 'KYC'), ('crm', 'CRM'), ('customer_credit', 'CC (Customer Credit)'), ('customer_strategy', 'CS (Customer Strategy)'),('vrm', 'VRM'), ('vendor_credit', 'VC (Vendor Credit)'), ('vendor_strategy', 'VS (Vendor Strategy)')], string='Application Type')
    application_request_type = fields.Selection([('new','New'),('review','Review'),('amend','Amend')], default="new", string="Request Type")
    #application_purpose_note = fields.Html("Purpose")
    #application_justification_note = fields.Html("Justification")
    expiry_date_formula = fields.Selection([('1y', '1 Year'),('6m', '6 Months'),('3m', '3 Months'),('specific', 'Specific')], default="1y", string='Expiry Date', help="Expiry date of the application")
    expiry_date = fields.Date(string="Expiry Date")
    
    review_date_formula = fields.Selection([('3m', '3 Months'),('2m', '2 Months'),('1m', '1 Month'),('specific', 'Specific')], default="1m", string='Review Date', help="Period Before Expiry Date")
    review_date = fields.Date(string="Review Date", help="Due date of the next review")

    

    @api.onchange('expiry_date_formula','review_date_formula','expiry_date','review_date')
    def _update_expiry_review_dates(self):
        if self.expiry_date_formula == '3m':
            self.expiry_date = (fields.Datetime.now() + relativedelta(months=3)).astimezone(timezone(self.env.user.tz))
        elif self.expiry_date_formula == '6m':
            self.expiry_date = (fields.Datetime.now() + relativedelta(months=6)).astimezone(timezone(self.env.user.tz))
        elif self.expiry_date_formula == '1y':
            self.expiry_date = (fields.Datetime.now() + relativedelta(years=1)).astimezone(timezone(self.env.user.tz))
        elif self.expiry_date_formula == '2y':
            self.expiry_date = (fields.Datetime.now() + relativedelta(years=2)).astimezone(timezone(self.env.user.tz))
        

        if self.expiry_date:
            if self.review_date_formula == '1m':
                self.review_date = self.expiry_date - relativedelta(months=1) 
            elif self.review_date_formula == '2m':
                self.review_date = self.expiry_date - relativedelta(months=2) 
            elif self.review_date_formula == '3m':
                self.review_date = self.expiry_date - relativedelta(months=3) 
        
        if self.expiry_date:
            if self.expiry_date < fields.Date.today():
                raise UserError("Expiry Date is in the past")
        
        if self.review_date:
            if self.review_date < fields.Date.today():
                raise UserError("Review Date is in the past")

        if self.expiry_date and self.review_date:
            if self.review_date > self.expiry_date:
                raise UserError("Review Date cannot be after Expiry Date")
        
            


    ## COMMON KYC FIELDS
    company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], default="company")
    legal_name = fields.Char(string='Name', help="Official / Legal English Name")
    name_alt_lang = fields.Char(string='Name (AR)', help="Official / Legal Name (AR)")
    trade_name = fields.Char(string='Trading Name', translate=True, help="if different from Legal Entity Name")
    trade_name_alt_lang = fields.Char(string='Trading Name (AR)', translate=True, help="if different from Legal Entity Name")
    
    category_id = fields.Many2many('res.partner.category', 'partner_tags_application', 'application_partner_id' ,'application_category_id', string='Tags', help="Account tags can be used for filtering and reporting")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
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

    ## KYC - Duplication
    duplicate_approved = fields.Boolean('Duplicate Partner', default=False)

    @api.onchange('company_type')
    @api.depends('company_type')
    def clear_individual_fields(self):
        if self.company_type == 'company':
            self.function = False
            self.title = False

    
    #### CUSTOMER FIELDS

    # Customer CRM Fields
    
    user_id = fields.Many2one('res.users', string='Salesperson')
    team_id = fields.Many2one('crm.team', string='Sales Team', related="user_id.sale_team_id")
    customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", default="general", tracking=True)
    customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], default="retail", string="Customer Segment", tracking=True)
    customer_pricelist_ids = fields.Many2many('product.pricelist', 'customer_pricelists_application', 'pricelist_id', 'application_id', string="Customer Pricelists")
    deal_min_margin = fields.Float(string="Deal Min. Margin %", help="Specify a minimum target bundle margin per deal/order", default=0)


    ## Customer CRM - Business Info
    annual_revenues = fields.Monetary(string="Annual Revenues", help="Annual gross revenue/sales of the entity/person")
    employee_count = fields.Integer("Number of Employees")
    countries_covered = fields.Many2many('res.country', 'countries_covered_application', 'country_id', 'application_id', string='Countries of Business', help="Countries where the entity conduct business")    
    business_brief = fields.Html("Business Brief", help="Brief about the entity, business model, history, track record, market position, etc..")

    ## Customer CRM - Logistics Requirements
    account_requirements = fields.Html("Account Requirements", help="Service/products requirements, volumes, TEUs, type of goods, value of goods, etc..")
    #annual_teus = fields.Integer("Annual Volume in TEUs")
    #ship_type = fields.Selection([('pallet', 'Pallet'), ('container', 'Container'), ('bulk', 'Bulk'), ('others', 'Others')], string='Main Shipping Type')
    #goods_type = fields.Html("Goods Type")
    #goods_value = fields.Html("Goods Value")
    major_countries = fields.Many2many('res.country', 'countries_destinations_application', 'country_id', 'application_id', string='Major Origins/Destinations')
    services_needed = fields.Many2many('product.product', 'services_needed_application', 'product_id', 'application_id', string='Services/Products')
    service_categories_needed = fields.Many2many('product.category', 'service_categories_needed_application', 'product_category_id', 'application_id', string='Categories', compute='_get_services_needed_categories', store=True, compute_sudo=True, depends=['services_needed'])
    @api.depends('services_needed','services_needed.categ_id')
    def _get_services_needed_categories(self):
        for record in self:
            record.service_categories_needed = [(6,0,record.services_needed.categ_id.ids)]

    operation_brief = fields.Html("Operation Note", help="Brief explaination of the operation requirements of the account")
    
    # Customer Strategy Fields
    account_kpis = fields.Html("Client's KPIs", help="KPIs and metrics that the account is focusing on")
    client_projects = fields.Html("Client's Projects", help="Key Projects and outline how your business can help")
    client_profile = fields.Html("Client's Profile", help="Identify which job title(s) you are targeting, how many of those exist in the account you are planning for, and what use they have for your product.")
    client_history = fields.Html("Client's History", help="Briefly summarize or list out bullets on your history with this account. This should include initial outreach attempts, project status, and lifecycle stage.")
    stakeholders = fields.Html("Stakeholders", help="List out the main stakeholders you have or expect to have involved in this relationship from both your and your account side.")
    whitespace = fields.Html("Whitespace Analysis", help="Illustrate the whitespace you have for helping your account and how you plan on appealing to that gap.")
    sales_performance = fields.Html("Sales Performance", help="What is your revenue from this account (projected if the account is the prospect), and how does each individual product or service you offer contribute to that number?")
    margin_performance = fields.Html("Margin Performance", help="What is your profit from this account (projected if the account is the prospect), and how does each individual product or service you offer contribute to that number?")
    wins_losses = fields.Html("Wins &amp; Losses", help="Include actuals or projections for onboarding costs, upsells, downgrades, price increases, and/or churn rate over time.]")
    account_competitors = fields.Html("Competitors", help="List your account's key competitors")
    competitors_stregnths = fields.Html("Competitors Strengths", help="List your account's key strengths in comparison to its competition. This can be formatted as a list of strengths that the competition does not have, or as a chart comparing your company's strengths linearly to competitors")
    competitors_weaknesses = fields.Html("Competitors Weaknesses", help="List your account's key weaknesses in comparison to its competition. This can be formatted as a list of weaknesses that the competition does not have, or as a chart comparing your company's strengths linearly to competitors")
    buyer_journey = fields.Html("The Buyer's Journey", help="For existing accounts, explain the process of the buyer's journey - the timeline, the lifecycle stages, and where the account is now. For prospects, highlight a projected buyer's journey and the timeline for how you'll get the account from stranger to customer.")
    content_channels = fields.Html("Content &amp; Channels", help="Think about what information your buyers consume - specifically pertaining to your industry and your product - and where they might consume that information")
    evaluation_criteria = fields.Html("Evaluation Criteria", help="What factors does/did your account consider before purchasing, and do you fare in these categories, and what lessons did you learn about your performance in these categories for future sales?")
    decision_criteria = fields.Html("Key Decision Criteria", help="What factors are the most important for the person or people you sold (or are selling) to? How did you (or how do you expect to) win with your performance in these criteria?")
    relationship_current_status = fields.Html("Current Relationship Status", help="What are you to the account at this time? (Potential) Vendor, Preferred Supplier, Planning Partner, Trusted Advisor, etc.")
    relationship_target_status = fields.Html("Relationship Target", help="What relationship status or lifecycle stage do you want this account to achieve, and by when?")
    core_business_partners = fields.Html("Core Business Partners", help="Are any other accounts, companies, or customers involved in this relationship, and if so, to what extent?")
    relationship_progression_strategy = fields.Html("Relationship Progression Strategy", help="What process will you plan and execute on to progress your account to your desired stage?")
    services = fields.Html("Products &amp; Services", help="List the products(s) and service(s) you intend to sell or have sold to this account. Include each line item's price point, quantity, and how long each will last for the customer before renewal/reorder")
    sales_targets = fields.Html("Sales Targets", help="For the time period of your choosing, what are your revenue goals for this account?")
    cross_sell = fields.Html("Cross-sell &amp; Upsell Opportunities", help="Outside of previously listed opportunities, what can or will you pitch as a cross-sell or upsell opportunity as your relationship with the account strengthens over time?")
    risks_challenges = fields.Html("Risks &amp; Challenges", help="What issues lie in the way of selling, cross-selling, or upselling your account on any of the above mentioned line items? Address how you will counter them - if possible.")
    critical_resources = fields.Html("Critical Resources", help="List the resources available to your team for this project. Examples include your ERP/CRM, customer retention manuals, how to sell documentation, communication methods for the team, the account's company website, and more.")
    #project_ids = fields.Many2many('project.project', 'project_application', 'project_id', 'application_id', string="Customer Projects", help="Create or link Projects and tasks")

    # Customer Credit Fields
    monthly_expected_business = fields.Monetary(string="Monthly Expected Sales", help="Expected monthly account revenues")
    customer_credit_limit = fields.Monetary(string="Customer Credit Limit")
    credit_trade_references = fields.Html(string="Trade References", help="Please provide at least 3 Credit Trade References")
    #customer_payment_term_ids = fields.Many2many('account.payment.term', 'customer_payment_terms_application', 'term_id', 'application_id', string="Customer Payment Terms")
    customer_payment_term_ids = fields.Many2one('account.payment.term', string="Customer Payment Terms")

    #### VENDOR FIELDS

    # Vendor VRM Fields
    buyer_id = fields.Many2one('res.users', string='Purchase Manager')
    purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team', related="buyer_id.purchase_team_id")
    vendor_class = fields.Selection([('general','General Vendor'),('key','Key Vendor'),('strategic','Strategic Vendor')], string="Vendor Class", default="general", tracking=True)
    vendor_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], default="retail", string="Vendor Segment", tracking=True)
    vendor_currency_ids = fields.Many2many('res.currency', 'currencies_application', 'currency_id', 'application_id', string="Vendor Currencies", help="This currency will be used, instead of the default one, for purchases from the current partner")


    ## Vendor VRM - Business Info
    vendor_annual_revenues = fields.Monetary(string="Annual Revenues", help="Annual gross revenue/sales of the entity/person")
    vendor_employee_count = fields.Integer("Number of Employees")
    vendor_countries_covered = fields.Many2many('res.country', 'vendor_countries_covered_application', 'country_id', 'application_id', string='Countries of Business', help="Countries where the entity conduct business")    
    vendor_business_brief = fields.Html("Business Brief", help="Brief about the entity, business model, history, track record, market position, etc..")

    ## Vendor VRM - Logistics Requirements
    vendor_account_offerings = fields.Html("Account Offerings", help="Service/products provided, rates, etc..")
    vendor_major_countries = fields.Many2many('res.country', 'vendor_countries_destinations_application', 'country_id', 'application_id', string='Major Origins/Destinations')
    services_provided = fields.Many2many('product.product', 'vendor_services_needed_application', 'product_id', 'application_id', string='Services/Products')
    service_categories_provided = fields.Many2many('product.category', 'service_categories_provided_application', 'product_category_id', 'application_id', string='Categories', compute='_get_services_provided_categories', store=True, compute_sudo=True, depends=['services_provided'])
    @api.depends('services_needed','services_needed.categ_id')
    def _get_services_provided_categories(self):
        for record in self:
            record.service_categories_provided = [(6,0,record.services_provided.categ_id.ids)]
            
    vendor_operation_brief = fields.Html("Operation Note", help="Brief explaination of the operation requirements of the account")
    
    # Vendor Strategy Fields
    vendor_kpis = fields.Html("Vendor's KPIs", help="KPIs and metrics that the account is focusing on")
    vendor_projects = fields.Html("Vendor's Projects", help="Key Projects and outline how your business can benefit")
    vendor_profile = fields.Html("Vendor's Profile", help="Identify which job title(s) you are targeting, how many of those exist in the account you are planning for, and what use they have for your product.")
    vendor_history = fields.Html("Client's History", help="Briefly summarize or list out bullets on your history with this account. This should include initial outreach attempts, project status, and lifecycle stage.")
    vendor_stakeholders = fields.Html("Stakeholders", help="List out the main stakeholders you have or expect to have involved in this relationship from both your and your account side.")
    vendor_whitespace = fields.Html("Whitespace Analysis", help="Illustrate the whitespace you have for helping your account and how you plan on appealing to that gap.")
    purchases_performance = fields.Html("Sales Performance", help="What is your volume from this account (projected if the account is the prospect), and how does each individual product or service you buy contribute to that number?")
    vendor_wins_losses = fields.Html("Wins &amp; Losses", help="Include actuals or projections for onboarding costs, upsells, downgrades, price increases, and/or churn rate over time.]")
    vendor_competitors = fields.Html("Competitors", help="List your account's key competitors")
    vendor_competitors_stregnths = fields.Html("Competitors Strengths", help="List your account's key strengths in comparison to its competition. This can be formatted as a list of strengths that the competition does not have, or as a chart comparing your company's strengths linearly to competitors")
    vendor_competitors_weaknesses = fields.Html("Competitors Weaknesses", help="List your account's key weaknesses in comparison to its competition. This can be formatted as a list of weaknesses that the competition does not have, or as a chart comparing your company's strengths linearly to competitors")
    selling_journey = fields.Html("The Seller's Journey", help="For existing accounts, explain the process of the seller's journey - the timeline, the lifecycle stages, and where the account is now. For prospects, highlight a projected seller's journey and the timeline for how you'll get the account from stranger to vendor.")
    vendor_content_channels = fields.Html("Content &amp; Channels", help="Think about what information your sellers consume - specifically pertaining to your industry and your product - and where they might consume that information")
    vendor_evaluation_criteria = fields.Html("Evaluation Criteria", help="What factors does/did your account consider before purchasing, and do you fare in these categories, and what lessons did you learn about your performance in these categories for future sales?")
    vendor_decision_criteria = fields.Html("Key Decision Criteria", help="What factors are the most important for the person or people you sold (or are selling) to? How did you (or how do you expect to) win with your performance in these criteria?")
    vendor_relationship_current_status = fields.Html("Current Relationship Status", help="What are you to the account at this time? (Potential) Client, Preferred Client, Planning Partner, Strategic Client, etc.")
    vendor_relationship_target_status = fields.Html("Relationship Target", help="What relationship status or lifecycle stage do you want this account to achieve, and by when?")
    vendor_core_business_partners = fields.Html("Core Business Partners", help="Are any other accounts, companies, or vendors involved in this relationship, and if so, to what extent?")
    vendor_relationship_progression_strategy = fields.Html("Relationship Progression Strategy", help="What process will you plan and execute on to progress your account to your desired stage?")
    vendor_services = fields.Html("Products &amp; Services", help="List the products(s) and service(s) you intend to buy or have bought to this account. Include each line item's price point, quantity, and how long each will last for the vendor before renewal/reorder")
    purchases_targets = fields.Html("Procurement Targets", help="For the time period of your choosing, what are your procurement goals for this account?")
    vendor_risks_challenges = fields.Html("Risks &amp; Challenges", help="What issues lie in the way of buying on any of the above mentioned line items? Address how you will counter them - if possible.")
    vendor_critical_resources = fields.Html("Critical Resources", help="List the resources available to your team for this project. Examples include your ERP/CRM, customer retention manuals, how to sell documentation, communication methods for the team, the account's company website, and more.")
    #vendor_project_ids = fields.Many2many('project.project', 'project_vendor_application', 'project_id', 'application_id', string="Vendor Projects", help="Create or link Projects and tasks")

    # Vendor Credit Fields
    vendor_monthly_expected_business = fields.Monetary(string="Monthly Expected Procurement", help="Expected monthly account purchases")
    vendor_credit_limit = fields.Monetary(string="Vendor Credit Limit")
    #vendor_payment_term_ids = fields.Many2many('account.payment.term', 'vendor_payment_terms_application', 'term_id', 'application_id', string="Vendor Payment Terms")
    vendor_payment_term_ids = fields.Many2one('account.payment.term', string="Vendor Payment Terms")

    #attachment fields
    attachment_ids = fields.One2many('res.partner.application.attachment','application_id', string="Attachments")

    #user action fields
    user_action_ids = fields.One2many('res.partner.application.user.action','application_id', string="User Actions")

        
 
                            



    # Previous application fields
    
    ## PREVIOUS COMMON KYC FIELDS
    previous_company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], related="current_kyc_id.company_type")
    previous_legal_name = fields.Char(string='English Official Name', related="current_kyc_id.legal_name")
    previous_name_alt_lang = fields.Char(string='Arabic Official Name', related="current_kyc_id.name_alt_lang")
    previous_trade_name = fields.Char(string='Trading Name', related="current_kyc_id.trade_name")
    previous_trade_name_alt_lang = fields.Char(string='Trading Name', related="current_kyc_id.trade_name_alt_lang")
    
    previous_category_id = fields.Many2many('res.partner.category', 'partner_tags_previous_application', 'application_partner_id' ,'application_category_id', string='Tags', related="current_kyc_id.category_id")
    previous_street = fields.Char(related="current_kyc_id.street")
    previous_street2 = fields.Char(related="current_kyc_id.street2")
    previous_zip = fields.Char(related="current_kyc_id.zip")
    previous_city = fields.Char(related="current_kyc_id.city")
    previous_state_id = fields.Many2one("res.country.state", string='State', related="current_kyc_id.state_id")
    previous_country_id = fields.Many2one('res.country', string='Country',related="current_kyc_id.country_id")
    previous_country_code = fields.Char(string="Country Code", related='previous_country_id.code')
    previous_l10n_sa_edi_building_number = fields.Char("Building Number",related="current_kyc_id.l10n_sa_edi_building_number")
    previous_l10n_sa_edi_plot_identification = fields.Char("Plot Identification",related="current_kyc_id.l10n_sa_edi_plot_identification")

    previous_email = fields.Char(related="current_kyc_id.email")
    previous_phone = fields.Char(related="current_kyc_id.phone")
    previous_mobile = fields.Char(related="current_kyc_id.mobile")
    previous_website = fields.Char(string='Website Link', related="current_kyc_id.website")
    previous_company_registry = fields.Char(related="current_kyc_id.company_registry", string="Official ID")
    previous_company_registry_expiry_date = fields.Date(string="Official ID Expiry", related="current_kyc_id.company_registry_expiry_date")
    previous_vat = fields.Char(related="current_kyc_id.vat", string='Tax ID')
    previous_ref = fields.Char(related="current_kyc_id.ref", string='Reference')

    ## Previous KYC - Companies
    previous_legal_type = fields.Selection([('establishment','Establishment'),('joint_liability','Joint Liability Company'),('limited_partnership','Limited Partnership Company'),('simple_joint','Simple Joint Stock Company'),('closed_joint','Closed Joint Stock Company'),('public','Public Joint Stock Company'),('llc','Limited Liability Company'),('one_llc','One Person Limited Liability Company')], related="current_kyc_id.legal_type")
    previous_industry_id = fields.Many2one('res.partner.industry', string="Industry", related="current_kyc_id.industry_id")
    previous_paidup_capital = fields.Monetary(string="Paid-up Capital", related="current_kyc_id.paidup_capital")
    previous_ownership_structure = fields.Html(string="Ownership Structure", related="current_kyc_id.ownership_structure")
    previous_management_structure = fields.Html(string="Management Structure", related="current_kyc_id.management_structure")
    previous_year_founded = fields.Char(string="Year Founded", related="current_kyc_id.year_founded")

    ## Previous KYC - Individuals
    previous_function = fields.Char(string="Job Position", related="current_kyc_id.function")
    previous_title = fields.Many2one('res.partner.title', string="Title", related="current_kyc_id.title")

    ## Previous KYC - Duplication
    previous_duplicate_approved = fields.Boolean('Duplicate Partner')


    #### PREVIOUS CUSTOMER FIELDS

    # Previous Customer CRM Fields
    
    previous_user_id = fields.Many2one('res.users', string='Salesperson', related="current_crm_id.user_id")
    previous_team_id = fields.Many2one('crm.team', string='Sales Team', related="current_crm_id.team_id")
    previous_customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", related="current_crm_id.customer_class")
    previous_customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], string="Customer Segment", related="current_crm_id.customer_segment")
    previous_customer_pricelist_ids = fields.Many2many('product.pricelist', 'customer_pricelists_previous_application', 'pricelist_id', 'application_id', string="Customer Pricelists", related="current_crm_id.customer_pricelist_ids")
    previous_deal_min_margin = fields.Float(string="Deal Min. Margin %", related="current_crm_id.deal_min_margin")

    ## Previous Customer CRM - Business Info
    previous_annual_revenues = fields.Monetary(string="Annual Revenues", related="current_crm_id.annual_revenues")
    previous_employee_count = fields.Integer("Number of Employees", related="current_crm_id.employee_count")
    previous_countries_covered = fields.Many2many('res.country', 'countries_covered_application', 'country_id', 'application_id', string='Countries of Business', related="current_crm_id.countries_covered")  
    previous_business_brief = fields.Html("Business Brief", related="current_crm_id.business_brief")

    ## Previous Customer CRM - Logistics Requirements
    previous_account_requirements = fields.Html("Account Requirements", related="current_crm_id.account_requirements")
    #previous_annual_teus = fields.Integer("Annual Volume in TEUs", related="current_crm_id.annual_teus")
    #previous_ship_type = fields.Selection([('pallet', 'Pallet'), ('container', 'Container'), ('bulk', 'Bulk'), ('others', 'Others')], string='Main Shipping Type', related="current_crm_id.ship_type")
    #previous_goods_type = fields.Html("Goods Type", related="current_crm_id.goods_type")
    #previous_goods_value = fields.Html("Goods Value", related="current_crm_id.goods_value")
    previous_major_countries = fields.Many2many('res.country', 'countries_destinations_application', 'country_id', 'application_id', string='Major Origins/Destinations', related="current_crm_id.major_countries")
    previous_services_needed = fields.Many2many('product.product', 'previous_services_needed_application', 'product_id', 'previous_application_id', string='Services', related="current_crm_id.services_needed")
    previous_service_categories_needed = fields.Many2many('product.category', 'previous_service_categories_needed_application', 'product_category_id', 'previous_application_id', string='Categories', related="current_crm_id.service_categories_needed")

    previous_operation_brief = fields.Html("Operation Note", related="current_crm_id.operation_brief")
    
    # Previous Customer Credit Fields
    previous_monthly_expected_business = fields.Monetary(string="Monthly Expected Sales", related="current_customer_credit_id.monthly_expected_business")
    previous_customer_credit_limit = fields.Monetary(string="Customer Credit Limit", related="current_customer_credit_id.customer_credit_limit")
    previous_credit_trade_references = fields.Html(string="Trade References", related="current_customer_credit_id.credit_trade_references")
    #previous_customer_payment_term_ids = fields.Many2many('account.payment.term', 'customer_payment_terms_previous_application', 'term_id', 'application_id', string="Customer Payment Terms", related="current_customer_credit_id.customer_payment_term_ids")
    previous_customer_payment_term_ids = fields.Many2one('account.payment.term', string="Customer Payment Terms", related="current_customer_credit_id.customer_payment_term_ids")

    # Previous Customer Strategy Fields
    previous_account_kpis = fields.Html("Client's KPIs", related="current_customer_strategy_id.account_kpis")
    previous_client_projects = fields.Html("Client's Projects", related="current_customer_strategy_id.client_projects")
    previous_client_profile = fields.Html("Client's Profile", related="current_customer_strategy_id.client_profile")
    previous_client_history = fields.Html("Client's History", related="current_customer_strategy_id.client_history")
    previous_stakeholders = fields.Html("Stakeholders", related="current_customer_strategy_id.stakeholders")
    previous_whitespace = fields.Html("Whitespace Analysis", related="current_customer_strategy_id.whitespace")
    previous_sales_performance = fields.Html("Sales Performance", related="current_customer_strategy_id.sales_performance")
    previous_margin_performance = fields.Html("Margin Performance", related="current_customer_strategy_id.margin_performance")
    previous_wins_losses = fields.Html("Wins &amp; Losses", related="current_customer_strategy_id.wins_losses")
    previous_account_competitors = fields.Html("Competitors", related="current_customer_strategy_id.account_competitors")
    previous_competitors_stregnths = fields.Html("Competitors Strengths", related="current_customer_strategy_id.competitors_stregnths")
    previous_competitors_weaknesses = fields.Html("Competitors Weaknesses", related="current_customer_strategy_id.competitors_weaknesses")
    previous_buyer_journey = fields.Html("The Buyer's Journey", related="current_customer_strategy_id.buyer_journey")
    previous_content_channels = fields.Html("Content &amp; Channels", related="current_customer_strategy_id.content_channels")
    previous_evaluation_criteria = fields.Html("Evaluation Criteria", related="current_customer_strategy_id.evaluation_criteria")
    previous_decision_criteria = fields.Html("Key Decision Criteria", related="current_customer_strategy_id.decision_criteria")
    previous_relationship_current_status = fields.Html("Current Relationship Status", related="current_customer_strategy_id.relationship_current_status")
    previous_relationship_target_status = fields.Html("Relationship Target", related="current_customer_strategy_id.relationship_target_status")
    previous_core_business_partners = fields.Html("Core Business Partners", related="current_customer_strategy_id.core_business_partners")
    previous_relationship_progression_strategy = fields.Html("Relationship Progression Strategy", related="current_customer_strategy_id.relationship_progression_strategy")
    previous_services = fields.Html("Products &amp; Services", related="current_customer_strategy_id.services")
    previous_sales_targets = fields.Html("Sales Targets", related="current_customer_strategy_id.sales_targets")
    previous_cross_sell = fields.Html("Cross-sell &amp; Upsell Opportunities", related="current_customer_strategy_id.cross_sell")
    previous_risks_challenges = fields.Html("Risks &amp; Challenges", related="current_customer_strategy_id.risks_challenges")
    previous_critical_resources = fields.Html("Critical Resources", related="current_customer_strategy_id.critical_resources")
    #previous_project_ids = fields.Many2many('project.project', 'project_previous_application', 'project_id', 'application_id', string="Customer Projects", related="current_customer_strategy_id.project_ids")

    



    #### VENDOR FIELDS

    # Vendor VRM Fields
    previous_buyer_id = fields.Many2one('res.users', string='Purchase Manager', related="current_vrm_id.buyer_id")
    previous_purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team', related="current_vrm_id.purchase_team_id")
    previous_vendor_class = fields.Selection([('general','General Vendor'),('key','Key Vendor'),('strategic','Strategic Vendor')], string="Vendor Class", related="current_vrm_id.vendor_class")
    previous_vendor_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], string="Vendor Segment", related="current_vrm_id.vendor_segment")
    previous_vendor_currency_ids = fields.Many2many('res.currency', 'currencies_previous_application', 'currency_id', 'application_id', string="Vendor Currencies", related="current_vrm_id.vendor_currency_ids")


    ## Vendor VRM - Business Info
    previous_vendor_annual_revenues = fields.Monetary(string="Annual Revenues", related="current_vrm_id.vendor_annual_revenues")
    previous_vendor_employee_count = fields.Integer("Number of Employees", related="current_vrm_id.vendor_employee_count")
    previous_vendor_countries_covered = fields.Many2many('res.country', 'vendor_countries_covered_previous_application', 'country_id', 'application_id', string='Countries of Business', related="current_vrm_id.vendor_countries_covered")
    previous_vendor_business_brief = fields.Html("Business Brief", related="current_vrm_id.vendor_business_brief")

    ## Vendor VRM - Logistics Requirements
    previous_vendor_account_offerings = fields.Html("Account Offerings", related="current_vrm_id.vendor_account_offerings")
    previous_vendor_major_countries = fields.Many2many('res.country', 'vendor_countries_destinations_previous_application', 'country_id', 'application_id', string='Major Origins/Destinations', related="current_vrm_id.vendor_major_countries")
    previous_services_provided = fields.Many2many('product.product', 'vendor_previous_services_needed_previous_application', 'product_id', 'previous_application_id', string='Services', related="current_vrm_id.services_provided")
    previous_service_categories_provided = fields.Many2many('product.category', 'previous_service_categories_provided_application', 'product_category_id', 'previous_application_id', string='Categories', related="current_crm_id.service_categories_provided")
    previous_vendor_operation_brief = fields.Html("Operation Note", related="current_vrm_id.vendor_operation_brief")
    
    # Vendor Credit Fields
    previous_vendor_monthly_expected_business = fields.Monetary(string="Monthly Expected Procurement", related="current_vendor_credit_id.vendor_monthly_expected_business")
    previous_vendor_credit_limit = fields.Monetary(string="Credit Limit", related="current_vendor_credit_id.vendor_credit_limit")
    #previous_vendor_payment_term_ids = fields.Many2many('account.payment.term', 'vendor_payment_terms_previous_application', 'term_id', 'application_id', string="Vendor Payment Terms", related="current_vendor_credit_id.vendor_payment_term_ids")
    previous_vendor_payment_term_ids = fields.Many2one('account.payment.term', string="Vendor Payment Terms", related="current_vendor_credit_id.vendor_payment_term_ids")

    # Vendor Strategy Fields
    previous_vendor_kpis = fields.Html("Vendor's KPIs", related="current_vendor_strategy_id.vendor_kpis")
    previous_vendor_projects = fields.Html("Vendor's Projects", related="current_vendor_strategy_id.vendor_projects")
    previous_vendor_profile = fields.Html("Vendor's Profile", related="current_vendor_strategy_id.vendor_profile")
    previous_vendor_history = fields.Html("Client's History", related="current_vendor_strategy_id.vendor_history")
    previous_vendor_stakeholders = fields.Html("Stakeholders", related="current_vendor_strategy_id.vendor_stakeholders")
    previous_vendor_whitespace = fields.Html("Whitespace Analysis", related="current_vendor_strategy_id.vendor_whitespace")
    previous_purchases_performance = fields.Html("Sales Performance", related="current_vendor_strategy_id.purchases_performance")
    previous_vendor_wins_losses = fields.Html("Wins &amp; Losses", related="current_vendor_strategy_id.vendor_wins_losses")
    previous_vendor_competitors = fields.Html("Competitors", related="current_vendor_strategy_id.vendor_competitors")
    previous_vendor_competitors_stregnths = fields.Html("Competitors Strengths", related="current_vendor_strategy_id.vendor_competitors_stregnths")
    previous_vendor_competitors_weaknesses = fields.Html("Competitors Weaknesses", related="current_vendor_strategy_id.vendor_competitors_weaknesses")
    previous_selling_journey = fields.Html("The Seller's Journey", related="current_vendor_strategy_id.selling_journey")
    previous_vendor_content_channels = fields.Html("Content &amp; Channels", related="current_vendor_strategy_id.vendor_content_channels")
    previous_vendor_evaluation_criteria = fields.Html("Evaluation Criteria", related="current_vendor_strategy_id.vendor_evaluation_criteria")
    previous_vendor_decision_criteria = fields.Html("Key Decision Criteria", related="current_vendor_strategy_id.vendor_decision_criteria")
    previous_vendor_relationship_current_status = fields.Html("Current Relationship Status", related="current_vendor_strategy_id.vendor_relationship_current_status")
    previous_vendor_relationship_target_status = fields.Html("Relationship Target", related="current_vendor_strategy_id.vendor_relationship_target_status")
    previous_vendor_core_business_partners = fields.Html("Core Business Partners", related="current_vendor_strategy_id.vendor_core_business_partners")
    previous_vendor_relationship_progression_strategy = fields.Html("Relationship Progression Strategy", related="current_vendor_strategy_id.vendor_relationship_progression_strategy")
    previous_vendor_services = fields.Html("Products &amp; Services", related="current_vendor_strategy_id.vendor_services")
    previous_purchases_targets = fields.Html("Procurement Targets", related="current_vendor_strategy_id.purchases_targets")
    previous_vendor_risks_challenges = fields.Html("Risks &amp; Challenges", related="current_vendor_strategy_id.vendor_risks_challenges")
    previous_vendor_critical_resources = fields.Html("Critical Resources", related="current_vendor_strategy_id.vendor_critical_resources")
    #previous_vendor_project_ids = fields.Many2many('project.project', 'project_vendor_previous_application', 'project_id', 'application_id', string="Vendor Projects", related="current_vendor_strategy_id.vendor_project_ids")

    
    ####check duplication fields
    same_pa_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID', compute='_compute_same_pa_partner_id', store=False)
    same_pa_company_registry_partner_id = fields.Many2one('res.partner', string='Partner with same Company Registry', compute='_compute_same_pa_partner_id', store=False)
    same_pa_name_partner_id = fields.Many2one('res.partner', string='Partner with same Name', compute='_compute_same_pa_partner_id', store=False)
    same_pa_website_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_email_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_phone_partner_id = fields.Many2one('res.partner', string='Partner with same Phone', compute='_compute_same_pa_partner_id', store=False)
    same_pa_mobile_partner_id = fields.Many2one('res.partner', string='Partner with same Mobile', compute='_compute_same_pa_partner_id', store=False)
    

    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'legal_name','website','email','phone','mobile')
    #@api.onchange('vat', 'company_id', 'company_registry', 'country_id', 'legal_name','website','email','phone','mobile')
    def _compute_same_pa_partner_id(self):
        for partner in self.sudo():
            partner.same_pa_vat_partner_id = False
            partner.same_pa_company_registry_partner_id = False
            partner.same_pa_name_partner_id = False
            partner.same_pa_website_partner_id = False
            partner.same_pa_email_partner_id = False
            partner.same_pa_phone_partner_id = False
            partner.same_pa_mobile_partner_id = False

            if not partner.partner_id.duplicate_approved:
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
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
                
                partner.same_pa_company_registry_partner_id = bool(partner.company_registry) and Partner.search(domain, limit=1)

                # check name
                domain = [
                    ('name', 'ilike', partner.legal_name),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
                partner.same_pa_name_partner_id = bool(partner.legal_name) and Partner.search(domain, limit=1)

                # check website
                domain = [
                    ('website', '=', partner.website),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
                partner.same_pa_website_partner_id = bool(partner.website) and Partner.search(domain, limit=1)

                # check email
                domain = [
                    ('email', '=', partner.email),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
                partner.same_pa_email_partner_id = bool(partner.email) and Partner.search(domain, limit=1)

                # check phone
                domain = [
                    ('phone', '=', partner.phone),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
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
                if partner.partner_id.parent_id:
                    domain += [('id', '!=', partner.partner_id.parent_id.id)]
                partner.same_pa_mobile_partner_id = bool(partner.mobile) and Partner.search(domain, limit=1)


    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            
            #create name
            application_re = "GES/MEMO"
            values['name'] = application_re + self.env['ir.sequence'].next_by_code('res.partner.application') or _('New')
            
            #create user_action_id
            datas = {
                'user_id':self.env.user.id,
                'action':'created',
                'action_datetime': fields.Datetime.now(),
            }
            values['user_action_ids'] = [(0, 0, datas)]
            
        result = super(ResPartnerApplication, self).create(values)
        
        
        return result

    """
    @api.depends('application_direction','is_kyc','is_crm','is_customer_credit','is_customer_strategy','is_vrm','is_vendor_credit','is_vendor_strategy')
    def _get_application_types(self):
        for record in self:
            applicationtypes = []
            applicationtypes.append("KYC") if record.is_kyc else None
            applicationtypes.append("CRM") if record.is_crm and record.application_direction == 'customer' else None
            applicationtypes.append("Customer Credit") if record.is_customer_credit and record.application_direction == 'customer' else None
            applicationtypes.append("Account Strategy") if record.is_customer_strategy and record.application_direction == 'customer' else None
            applicationtypes.append("VRM") if record.is_vrm and record.application_direction == 'vendor' else None
            applicationtypes.append("Vendor Credit") if record.is_vendor_credit and record.application_direction == 'vendor' else None
            applicationtypes.append("Vendor Strategy") if record.is_vendor_strategy and record.application_direction == 'vendor' else None
            record.application_types = str(', '.join(applicationtypes))
    """
    def _copy_previous_kyc_basic_info(self):
        self.company_type = self.previous_company_type
        self.legal_name = self.previous_legal_name
        self.name_alt_lang = self.previous_name_alt_lang
        self.trade_name = self.previous_trade_name
        self.trade_name_alt_lang = self.previous_trade_name_alt_lang
        self.category_id = self.previous_category_id.ids
        self.company_registry = self.previous_company_registry
        self.company_registry_expiry_date = self.previous_company_registry_expiry_date
        self.vat = self.previous_vat
        self.ref = self.previous_ref
        self.legal_type = self.previous_legal_type
        self.function = self.previous_function
        self.title = self.previous_title
        self.duplicate_approved = self.previous_duplicate_approved
        
    def _copy_previous_kyc_address_info(self):
        self.street = self.previous_street
        self.street2 = self.previous_street2
        self.zip = self.previous_zip
        self.city = self.previous_city
        self.state_id = self.state_id.id
        self.country_id = self.previous_country_id.id
        self.l10n_sa_edi_building_number = self.previous_l10n_sa_edi_building_number
        self.l10n_sa_edi_plot_identification = self.previous_l10n_sa_edi_plot_identification


    def _copy_previous_kyc_contact_info(self):
        self.email = self.previous_email
        self.phone = self.previous_phone
        self.mobile = self.previous_mobile
        self.website = self.previous_website

    def _copy_previous_kyc_business_info(self):
        self.industry_id = self.previous_industry_id.id
        self.paidup_capital = self.previous_paidup_capital
        self.ownership_structure = self.previous_ownership_structure
        self.management_structure = self.previous_management_structure
        self.year_founded = self.previous_year_founded

    def _copy_previous_crm_segmentation_info(self):
        self.user_id = self.previous_user_id.id
        self.customer_class = self.previous_customer_class
        self.customer_segment = self.previous_customer_segment
        self.customer_pricelist_ids = self.previous_customer_pricelist_ids.ids
        self.deal_min_margin = self.previous_deal_min_margin

    def _copy_previous_crm_customer_business_info(self):
        self.annual_revenues = self.previous_annual_revenues
        self.employee_count = self.previous_employee_count
        self.countries_covered = self.previous_countries_covered.ids
        self.business_brief = self.previous_business_brief
    
    def _copy_previous_crm_customer_logistics_info(self):
        self.account_requirements = self.previous_account_requirements
        #self.annual_teus = self.previous_annual_teus
        #self.ship_type = self.previous_ship_type
        #self.goods_type = self.previous_goods_type
        #self.goods_value = self.previous_goods_value
        self.major_countries = self.previous_major_countries.ids

    def _copy_previous_crm_account_operations_info(self):
        self.services_needed = self.previous_services_needed.ids
        self.service_categories_needed = self.previous_service_categories_needed.ids
        self.operation_brief = self.previous_operation_brief

    def _copy_previous_customer_credit_info(self):
        self.monthly_expected_business = self.previous_monthly_expected_business
        self.customer_credit_limit = self.previous_customer_credit_limit
        self.customer_payment_term_ids = self.previous_customer_payment_term_ids.ids
        self.credit_trade_references = self.previous_credit_trade_references

    def _copy_previous_customer_strategy_info(self):
        self.account_kpis = self.previous_account_kpis
        self.client_projects = self.previous_client_projects
        self.client_profile = self.previous_client_profile
        self.client_projects = self.previous_client_projects
        self.client_history = self.previous_client_history
        self.stakeholders = self.previous_stakeholders
        self.whitespace = self.previous_whitespace
        self.sales_performance = self.previous_sales_performance
        self.margin_performance = self.previous_margin_performance
        self.wins_losses = self.previous_wins_losses
        self.account_competitors = self.previous_account_competitors
        self.competitors_stregnths = self.previous_competitors_stregnths
        self.competitors_weaknesses = self.previous_competitors_weaknesses
        self.buyer_journey = self.previous_buyer_journey
        self.content_channels = self.previous_content_channels
        self.evaluation_criteria = self.previous_evaluation_criteria
        self.decision_criteria = self.previous_decision_criteria
        self.relationship_current_status = self.previous_relationship_current_status
        self.relationship_target_status = self.previous_relationship_target_status
        self.core_business_partners = self.previous_core_business_partners
        self.relationship_progression_strategy = self.previous_relationship_progression_strategy
        self.services = self.previous_services
        self.sales_targets = self.previous_sales_targets
        self.cross_sell = self.previous_cross_sell
        self.risks_challenges = self.previous_risks_challenges
        self.critical_resources = self.previous_critical_resources
        #self.project_ids = self.previous_project_ids.ids
    
    def _copy_previous_vrm_segmentation_info(self):
        self.buyer_id = self.previous_buyer_id.id
        self.vendor_class = self.previous_vendor_class
        self.vendor_segment = self.previous_vendor_segment
        self.vendor_currency_ids = self.previous_vendor_currency_ids.ids
    
    def _copy_previous_vrm_vendor_business_info(self):
        self.vendor_annual_revenues = self.previous_vendor_annual_revenues
        self.vendor_employee_count = self.previous_vendor_employee_count
        self.vendor_countries_covered = self.previous_vendor_countries_covered.ids
        self.vendor_business_brief = self.previous_vendor_business_brief

    def _copy_previous_vrm_vendor_operations_info(self):
        self.vendor_account_offerings = self.previous_vendor_account_offerings
        self.vendor_major_countries = self.previous_vendor_major_countries.ids
        self.services_provided = self.previous_services_provided.ids
        self.service_categories_provided = self.previous_service_categories_provided.ids
        self.vendor_operation_brief = self.previous_vendor_operation_brief

    def _copy_previous_vendor_credit_info(self):
        self.vendor_monthly_expected_business = self.previous_vendor_monthly_expected_business
        self.vendor_credit_limit = self.previous_vendor_credit_limit
        self.vendor_payment_term_ids = self.previous_vendor_payment_term_ids.ids
    
    def _copy_previous_vendor_strategy_info(self):
        self.vendor_kpis = self.previous_vendor_kpis
        self.vendor_projects = self.previous_vendor_projects
        self.vendor_profile = self.previous_vendor_profile
        self.vendor_history = self.previous_vendor_history
        self.vendor_stakeholders = self.previous_vendor_stakeholders
        self.vendor_whitespace = self.previous_vendor_whitespace
        self.purchases_performance = self.previous_purchases_performance
        self.vendor_wins_losses = self.previous_vendor_wins_losses
        self.vendor_competitors = self.previous_vendor_competitors
        self.vendor_competitors_stregnths = self.previous_vendor_competitors_stregnths
        self.vendor_competitors_weaknesses = self.previous_vendor_competitors_weaknesses
        self.selling_journey = self.previous_selling_journey
        self.vendor_content_channels = self.previous_vendor_content_channels
        self.vendor_evaluation_criteria = self.previous_vendor_evaluation_criteria
        self.vendor_decision_criteria = self.previous_vendor_decision_criteria
        self.vendor_relationship_current_status = self.previous_vendor_relationship_current_status
        self.vendor_relationship_target_status = self.previous_vendor_relationship_target_status
        self.vendor_core_business_partners = self.previous_vendor_core_business_partners
        self.vendor_relationship_progression_strategy = self.previous_vendor_relationship_progression_strategy
        self.vendor_services = self.previous_vendor_services
        self.purchases_targets = self.previous_purchases_targets
        self.vendor_risks_challenges = self.previous_vendor_risks_challenges
        self.vendor_critical_resources = self.previous_vendor_critical_resources
        #self.vendor_project_ids = self.previous_vendor_project_ids

    




    def _copy_partner_kyc_to_new(self):
        self.company_type = self.partner_id.company_type
        self.legal_name = self.partner_id.name
        self.category_id = self.partner_id.category_id.ids
        self.company_registry = self.partner_id.company_registry
        self.vat = self.partner_id.vat
        self.ref = self.partner_id.ref
        self.function = self.partner_id.function
        self.title = self.partner_id.title      
        self.street = self.partner_id.street
        self.street2 = self.partner_id.street2
        self.zip = self.partner_id.zip
        self.city = self.partner_id.city
        self.state_id = self.state_id.id
        self.country_id = self.partner_id.country_id.id
        self.l10n_sa_edi_building_number = self.partner_id.l10n_sa_edi_building_number
        self.l10n_sa_edi_plot_identification = self.partner_id.l10n_sa_edi_plot_identification
        self.email = self.partner_id.email
        self.phone = self.partner_id.phone
        self.mobile = self.partner_id.mobile
        self.website = self.partner_id.website
        self.industry_id = self.partner_id.industry_id.id
        self.duplicate_approved = self.partner_id.duplicate_approved

    def _copy_partner_crm_to_new(self):
        self.user_id = self.partner_id.user_id.id
        self.customer_pricelist_ids = [(6,0, self.partner_id.property_product_pricelist.ids)]

    def _copy_partner_customer_credit_to_new(self):
        self.customer_payment_term_ids = [(6,0,self.partner_id.property_payment_term_id.ids)]

    def _copy_partner_vrm_to_new(self):
        self.buyer_id = self.partner_id.buyer_id.id
        self.vendor_currency_ids = [(6,0, self.partner_id.property_purchase_currency_id.ids)]
    
    def _copy_partner_vendor_credit_to_new(self):
        self.vendor_payment_term_ids = [(6,0, self.partner_id.property_supplier_payment_term_id.ids)]



    @api.onchange('application_request_type','partner_id','application_type')
    def _copy_previous_kyc(self):
        if self.application_type == 'kyc' and self.application_request_type in ('review','amend'):
            self._copy_previous_kyc_basic_info()
            self._copy_previous_kyc_address_info()
            self._copy_previous_kyc_contact_info()
            self._copy_previous_kyc_business_info()
        if self.application_type == 'crm' and self.application_request_type in ('review','amend'):
            self._copy_previous_crm_segmentation_info()
            self._copy_previous_crm_customer_business_info()
            self._copy_previous_crm_customer_logistics_info()
            self._copy_previous_crm_account_operations_info()
        if self.application_type == 'customer_credit' and self.application_request_type in ('review','amend'):
            self._copy_previous_customer_credit_info()
        if self.application_type == 'customer_strategy' and self.application_request_type in ('review','amend'):
            self._copy_previous_customer_strategy_info()
        if self.application_type == 'vrm' and self.application_request_type in ('review','amend'):
            self._copy_previous_vrm_segmentation_info()
            self._copy_previous_vrm_vendor_business_info()
            self._copy_previous_vrm_vendor_operations_info()
        if self.application_type == 'vendor_credit' and self.application_request_type in ('review','amend'):
            self._copy_previous_vendor_credit_info()
        if self.application_type == 'vendor_strategy' and self.application_request_type in ('review','amend'):
            self._copy_previous_vendor_strategy_info()

        if self.application_type == 'kyc' and self.application_request_type == 'new':
            self._copy_partner_kyc_to_new()
        if self.application_type == 'crm' and self.application_request_type == 'new':
            self._copy_partner_crm_to_new()
        if self.application_type == 'customer_credit' and self.application_request_type == 'new':
            self._copy_partner_customer_credit_to_new()
        if self.application_type == 'vrm' and self.application_request_type == 'new':
            self._copy_partner_vrm_to_new()
        if self.application_type == 'vendor_credit' and self.application_request_type == 'new':
            self._copy_partner_vendor_credit_to_new()
    

    def action_wizard_submit(self):

        return {
            'name': 'Submit Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'submitted'
                }
        }
       

    def _action_submit(self, note=False):
        for record in self:
            record.write({'state': 'submitted'})
            
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('user_id','=',self.env.user.id),('action','=','submitted')])
       
            # add user action
            datas = {
                'user_id': self.env.user.id,
                'action':'submitted' if not user_action_id else 'resubmitted',
                'action_datetime': fields.Datetime.now(),
                'note': note,
            }
            record.user_action_ids = [(0, 0, datas)] 
            
            # add pending actions for Validators

            with_user = self.env['ir.config_parameter'].sudo()
            user_ids = False
            if record.application_type == "kyc":
                user_ids = with_user.get_param('ges_logistics_partner.partner_kyc_validator_ids')
            elif record.application_type == "crm":
                user_ids = with_user.get_param('ges_logistics_partner.partner_crm_validator_ids')
            elif record.application_type == "customer_credit":
                user_ids = with_user.get_param('ges_logistics_partner.partner_customer_credit_validator_ids')
            elif record.application_type == "customer_strategy":
                user_ids = with_user.get_param('ges_logistics_partner.partner_customer_strategy_validator_ids')
            elif record.application_type == "vrm":
                user_ids = with_user.get_param('ges_logistics_partner.partner_vrm_validator_ids')
            elif record.application_type == "vendor_credit":
                user_ids = with_user.get_param('ges_logistics_partner.partner_vendor_credit_validator_ids')
            elif record.application_type == "vendor_strategy":
                user_ids = with_user.get_param('ges_logistics_partner.partner_vendor_strategy_validator_ids')

            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','in',literal_eval(user_ids))])
            if user_records:
                for user in user_records:
                    datas = {
                        'user_id': user.id,
                        'action':'pending_validation',
                        'action_datetime': fields.Datetime.now(),
                    }
                    record.user_action_ids = [(0, 0, datas)] if user_records else False
    
    def action_wizard_validate(self):

        return {
            'name': 'Validate Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'validated'
                }
        }
    
    def _action_validate(self, note=False):
        for record in self:
            ok_to_proceed = False
            
            # change pending action for current user(s)
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('user_id','=',self.env.user.id),('action','=','pending_validation')])

            if user_action_id:
                for uac in user_action_id:
                    datas = {
                        'user_id': self.env.user.id,
                        'action':'validated',
                        'action_datetime': fields.Datetime.now(),
                        'pending_timestamp': uac.action_datetime,
                        'note': note,
                    }
                    uac.write(datas)
            else:
                raise UserError("You cannot perform this action. Either already done or another user is required. (Error: No pending actions)")
                
            # change application status and/or other user actions depending on Application Type Decision Making - signly or jointly
            with_user = self.env['ir.config_parameter'].sudo()
            decision_making = False
            if record.application_type == "kyc":
                decision_making = with_user.get_param('ges_logistics_partner.partner_kyc_validator_ids_decision')
            elif record.application_type == "crm":
                decision_making = with_user.get_param('ges_logistics_partner.partner_crm_validator_ids_decision')
            elif record.application_type == "customer_credit":
                decision_making = with_user.get_param('ges_logistics_partner.partner_customer_credit_validator_ids_decision')
            elif record.application_type == "customer_strategy":
                decision_making = with_user.get_param('ges_logistics_partner.partner_customer_strategy_validator_ids_decision')
            elif record.application_type == "vrm":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vrm_validator_ids_decision')
            elif record.application_type == "vendor_credit":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vendor_credit_validator_ids_decision')
            elif record.application_type == "vendor_strategy":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vendor_strategy_validator_ids_decision')

            if decision_making == 'singly':
                ok_to_proceed = True
                user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_validation')])
                datas = {
                    'action':'validated_by_others',
                }
                user_action_id.write(datas)
            elif decision_making == 'jointly':
                user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_validation')])
                if not user_action_id:
                    ok_to_proceed = True
            
            if ok_to_proceed:
                record.write({'state': 'validated'})
                
                # add pending actions for next Action Takers
                
                with_user = self.env['ir.config_parameter'].sudo()
                user_ids = False
                if record.application_type == "kyc":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_kyc_approver_ids')
                elif record.application_type == "crm":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_crm_approver_ids')
                elif record.application_type == "customer_credit":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_customer_credit_approver_ids')
                elif record.application_type == "customer_strategy":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_customer_strategy_approver_ids')
                elif record.application_type == "vrm":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_vrm_approver_ids')
                elif record.application_type == "vendor_credit":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_vendor_credit_approver_ids')
                elif record.application_type == "vendor_strategy":
                    user_ids = with_user.get_param('ges_logistics_partner.partner_vendor_strategy_approver_ids')

                user_records = False
                if user_ids:
                    user_records = self.env['res.users'].search([('id','in',literal_eval(user_ids))])
                if user_records:
                    for user in user_records:
                        datas = {
                            'user_id': user.id,
                            'action':'pending_approval',
                            'action_datetime': fields.Datetime.now(),
                        }
                        record.user_action_ids = [(0, 0, datas)] if user_records else False

    def action_wizard_approve(self):

        return {
            'name': 'Approve Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'approved'
                }
        } 

    def _action_approve(self, note=False):
        for record in self:
            ok_to_proceed = False
            
            # change pending action for current user(s)
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('user_id','=',self.env.user.id),('action','=','pending_approval')])
            if user_action_id:
                datas = {
                    'user_id': self.env.user.id,
                    'action':'approved',
                    'action_datetime': fields.Datetime.now(),
                    'pending_timestamp': user_action_id.action_datetime,
                    'note': note,
                }
                user_action_id.write(datas)
            else:
                raise UserError("You cannot perform this action. Either already done or another user is required. (Error: No pending actions)")
                
            # change application status and/or other user actions depending on Application Type Decision Making - signly or jointly
            with_user = self.env['ir.config_parameter'].sudo()
            decision_making = False
            if record.application_type == "kyc":
                decision_making = with_user.get_param('ges_logistics_partner.partner_kyc_approver_ids_decision')
            elif record.application_type == "crm":
                decision_making = with_user.get_param('ges_logistics_partner.partner_crm_approver_ids_decision')
            elif record.application_type == "customer_credit":
                decision_making = with_user.get_param('ges_logistics_partner.partner_customer_credit_approver_ids_decision')
            elif record.application_type == "customer_strategy":
                decision_making = with_user.get_param('ges_logistics_partner.partner_customer_strategy_approver_ids_decision')
            elif record.application_type == "vrm":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vrm_approver_ids_decision')
            elif record.application_type == "vendor_credit":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vendor_credit_approver_ids_decision')
            elif record.application_type == "vendor_strategy":
                decision_making = with_user.get_param('ges_logistics_partner.partner_vendor_strategy_approver_ids_decision')
            
            if decision_making == 'singly':
                ok_to_proceed = True
                user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_approval')])
                datas = {
                    'action':'approved_by_others',
                }
                user_action_id.write(datas)
            elif decision_making == 'jointly':
                user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_approval')])
                if not user_action_id:
                    ok_to_proceed = True
            
            if ok_to_proceed:
                record.write({'state': 'approved'})
                record._action_activate()
            
    def action_wizard_reject(self):

        return {
            'name': 'Reject Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'rejected'
                }
        } 

    def _action_reject(self, note=False):
        for record in self:  
            # change pending action for current user(s)
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('user_id','=',self.env.user.id),('action','=','pending_approval')])
            if user_action_id:
                datas = {
                    'user_id': self.env.user.id,
                    'action':'rejected',
                    'action_datetime': fields.Datetime.now(),
                    'pending_timestamp': user_action_id.action_datetime,
                    'note': note,
                }
                user_action_id.write(datas)
            else:
                raise UserError("You cannot perform this action. Either already done or another user is required. (Error: No pending actions)")
                
            # change application status and/or other user actions depending on Application Type Decision Making - signly or jointly
            
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_approval')])
            datas = {
                'action':'rejected_by_others',
            }
            user_action_id.write(datas)
        
            record.write({'state': 'rejected'})
            

    def _action_activate(self):
        for record in self:
            

            #de-activate other active applications
            current_active_application = record.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=',record.application_type),('state','=','active'),('id','!=',record.id)])
            current_active_application.write({'state': 'cancel'})

            # add action for current user(s)
            datas = {
                'user_id': self.env.user.id,
                'action':'activated',
                'action_datetime': fields.Datetime.now(),
            }
            record.user_action_ids = [(0, 0, datas)] 
            record.write({'state': 'active'})

            #set active application on partner
            if record.application_type == "kyc":
                record.partner_id.current_kyc_id = record.id
            elif record.application_type == "crm":
                record.partner_id.current_crm_id = record.id
            elif record.application_type == "customer_credit":
                record.partner_id.current_customer_credit_id = record.id
            elif record.application_type == "customer_strategy":
                record.partner_id.current_customer_strategy_id = record.id
            elif record.application_type == "vrm":
                record.partner_id.current_vrm_id = record.id
            elif record.application_type == "vendor_credit":
                record.partner_id.current_vendor_credit_id = record.id
            elif record.application_type == "vendor_strategy":
                record.partner_id.current_vendor_strategy_id = record.id
            
            #update partner.active_application_ids
            record.partner_id.active_application_ids = [(4, record.id)]
            record.partner_id.active_application_ids = [(3, current_active_application.id)]

            #update partner fields
            partner_rec = record.with_context(through_partner_application=True)
            
            if record.application_type == "kyc":                
                partner_rec.partner_id.company_type = record.company_type
                partner_rec.partner_id.name = record.legal_name
                partner_rec.partner_id.name_alt_lang = record.name_alt_lang
                partner_rec.partner_id.trade_name = record.trade_name
                partner_rec.partner_id.trade_name_alt_lang = record.trade_name_alt_lang
                
                partner_rec.partner_id.category_id = record.category_id.ids
                partner_rec.partner_id.street = record.street
                partner_rec.partner_id.street2 = record.street2
                partner_rec.partner_id.zip = record.zip
                partner_rec.partner_id.city = record.city
                partner_rec.partner_id.state_id = record.state_id.id
                partner_rec.partner_id.country_id = record.country_id.id
                partner_rec.partner_id.l10n_sa_edi_building_number = record.l10n_sa_edi_building_number
                partner_rec.partner_id.l10n_sa_edi_plot_identification = record.l10n_sa_edi_plot_identification

                partner_rec.partner_id.email = record.email
                partner_rec.partner_id.phone = record.phone
                partner_rec.partner_id.mobile = record.mobile
                partner_rec.partner_id.website = record.website
                partner_rec.partner_id.company_registry = record.company_registry
                partner_rec.partner_id.vat = record.vat
                partner_rec.partner_id.ref = record.ref
                partner_rec.partner_id.industry_id = record.industry_id.id
                partner_rec.partner_id.function = record.function
                partner_rec.partner_id.title = record.title
                partner_rec.partner_id.duplicate_approved = record.duplicate_approved

            if record.application_type == "crm":
                partner_rec.partner_id.user_id = record.user_id.id
                partner_rec.partner_id.team_id = record.team_id.id
                partner_rec.partner_id.pa_user_id = record.user_id.id
                partner_rec.partner_id.pa_team_id = record.team_id.id
                if record.partner_id.pa_property_product_pricelist:
                    if record.partner_id.pa_property_product_pricelist.id not in record.customer_pricelist_ids.ids:
                        partner_rec.partner_id.property_product_pricelist = False
                        partner_rec.partner_id.pa_property_product_pricelist = False

            if record.application_type == "customer_credit":
                partner_rec.partner_id.property_payment_term_id = record.customer_payment_term_ids
                partner_rec.partner_id.pa_property_payment_term_id = record.customer_payment_term_ids

            if record.application_type == "vrm":
                partner_rec.partner_id.buyer_id = record.buyer_id.id
                partner_rec.partner_id.purchase_partner_team_id = record.purchase_team_id.id
                partner_rec.partner_id.pa_buyer_id = record.buyer_id.id
                if record.partner_id.pa_property_purchase_currency_id:
                    if record.partner_id.pa_property_purchase_currency_id.id not in record.vendor_currency_ids.ids:
                        partner_rec.partner_id.property_purchase_currency_id = False
                        partner_rec.partner_id.pa_property_purchase_currency_id = False


            if record.application_type == "vendor_credit":
                partner_rec.partner_id.property_supplier_payment_term_id = record.vendor_payment_term_ids
                partner_rec.partner_id.pa_property_supplier_payment_term_id = record.vendor_payment_term_ids


    def action_wizard_cancel(self):

        return {
            'name': 'Cancel Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'cancelled'
                }
        } 

    def _action_cancel(self, note=False):
        for record in self:
            # add action for current user(s)
            datas = {
                'user_id': self.env.user.id,
                'action':'cancelled',
                'action_datetime': fields.Datetime.now(),
                'note': note,
            }
            record.user_action_ids = [(0, 0, datas)] 
            record.write({'state': 'cancel'})

            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','in',['pending_validation','pending_approval'])])
            datas = {
                'action':'cancelled_by_others',
            }
            user_action_id.write(datas)

            #remove active application on partner
            if record.application_type == "kyc":
                record.partner_id.current_kyc_id == False
            elif record.application_type == "crm":
                record.partner_id.current_crm_id == False
            elif record.application_type == "customer_credit":
                record.partner_id.current_customer_credit_id == False
            elif record.application_type == "customer_strategy":
                record.partner_id.current_customer_strategy_id == False
            elif record.application_type == "vrm":
                record.partner_id.current_vrm_id == False
            elif record.application_type == "vendor_credit":
                record.partner_id.current_vendor_credit_id == False
            elif record.application_type == "vendor_strategy":
                record.partner_id.current_vendor_strategy_id == False

            #update partner.active_application_ids
            record.partner_id.active_application_ids = [(3, record.id)]

    def action_wizard_draft(self):

        return {
            'name': 'Return Application(s)',
            'view_mode': 'form',
            'res_model': 'res.partner.application.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_application_ids': self.ids,
                'default_name': 'returned'
                }
        } 

    def _action_draft(self, note=False):
        for record in self:  
            # change pending action for current user(s)
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('user_id','=',self.env.user.id),('action','=','pending_validation')])
            if user_action_id:
                datas = {
                    'user_id': self.env.user.id,
                    'action':'returned',
                    'action_datetime': fields.Datetime.now(),
                    'pending_timestamp': user_action_id.action_datetime,
                    'note': note,
                }
                user_action_id.write(datas)
            else:
                raise UserError("You cannot perform this action. Either already done or another user is required. (Error: No pending actions)")
                
            # change application status and/or other user actions depending on Application Type Decision Making - signly or jointly
            
            user_action_id = self.env['res.partner.application.user.action'].search([('application_id','=',record.id),('action','=','pending_validation')])
            datas = {
                'action':'returned_by_others',
            }
            user_action_id.write(datas)
        
            record.write({'state': 'draft'})         

    def _action_expire(self, note=False):
        for record in self:
            # add action for current user(s)
            datas = {
                'user_id': self.env.user.id,
                'action':'expired',
                'action_datetime': fields.Datetime.now(),
                'note': note,
            }
            record.user_action_ids = [(0, 0, datas)] 
            record.write({'state': 'expired'})

    def write(self, values):
        if 'state' in values:
            new_state = values.get('state')

            if new_state == 'validated' or self.state == 'validated':
                values['color'] = 7
                if not self.env.user.has_group(
                        'ges_logistics_partner.group_partner_application_user_validate'):
                    raise ValidationError(
                        _("Only Managers can perform that move!"))

            if new_state == 'approved' or self.state == 'approved':
                values['color'] = 8
                if not self.env.user.has_group(
                        'ges_logistics_partner.group_partner_application_user_approve'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            
            if new_state == 'active' or self.state == 'active':
                values['color'] = 10
                if not self.env.user.has_group(
                        'ges_logistics_partner.group_partner_application_user_activate'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            
            if new_state == 'cancel' or self.state == 'cancel':
                values['color'] = False
                if not self.env.user.has_group(
                        'ges_logistics_partner.group_partner_application_user_cancel'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))

            if new_state == 'draft' and self.state != 'draft':
                values['color'] = False
                if not self.env.user.has_group(
                        'ges_logistics_partner.group_partner_application_user_return_draft'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            
            if new_state == 'expired':
                values['color'] = 1

            if new_state == 'rejected':
                values['color'] = 1
            
            if new_state == 'submitted':
                values['color'] = 4
            
        if 'active' in values:
            if not self.env.user.has_group(
                    'ges_logistics_partner.group_partner_application_user_archive'):
                raise ValidationError(
                    _("Only Managers can perform that move!"))

        if 'is_late_review' in values:
            if values.get('is_late_review') == True:
                values['color'] = 2
            
        return super().write(values)

    @api.depends('partner_id')
    def _get_current_applications(self):
        for record in self:
            current_kyc = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','kyc'),('state','in',['active','expired'])])
            record.current_kyc_id = current_kyc[0] if current_kyc else False

            current_crm = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','crm'),('state','in',['active','expired'])])
            record.current_crm_id = current_crm[0] if current_crm else False

            current_customer_credit = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','customer_credit'),('state','in',['active','expired'])])
            record.current_customer_credit_id = current_customer_credit[0] if current_customer_credit else False

            current_customer_strategy = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','customer_strategy'),('state','in',['active','expired'])])
            record.current_customer_strategy_id = current_customer_strategy[0] if current_customer_strategy else False

            current_vrm = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','vrm'),('state','in',['active','expired'])])
            record.current_vrm_id = current_vrm[0] if current_vrm else False

            current_vendor_credit = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','vendor_credit'),('state','in',['active','expired'])])
            record.current_vendor_credit_id = current_vendor_credit[0] if current_vendor_credit else False

            current_vendor_strategy = self.env['res.partner.application'].search([('partner_id','=',record.partner_id.id),('application_type','=','vendor_strategy'),('state','in',['active','expired'])])
            record.current_vendor_strategy_id = current_vendor_strategy[0] if current_vendor_strategy else False

    @api.depends('name')
    @api.depends_context('show_type')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record._context.get('show_type'):
                if record.application_type == 'kyc':
                    name = "KYC"
                elif record.application_type == 'crm':
                    name = "CRM"
                elif record.application_type == 'customer_credit':
                    name = "CC"
                elif record.application_type == 'customer_strategy':
                    name = "CS"
                elif record.application_type == 'vrm':
                    name = "VRM"
                elif record.application_type == 'vendor_credit':
                    name = "VC"
                elif record.application_type == 'vendor_strategy':
                    name = "VS"
            record.display_name = name

    @api.onchange('partner_id','application_type','application_request_type')
    def _get_request_type_options(self):

        if self.partner_id:

            #check user permissions
            
            sale_user_not = self.partner_id.user_id != self.current_user_id and self.partner_id.user_id != False
            sale_team_not = self.partner_id.team_id != self.current_sale_team_id and self.partner_id.team_id != False
            all_sale_not = sale_user_not and sale_team_not
            
            purchase_user_not = self.partner_id.buyer_id != self.current_user_id and self.partner_id.buyer_id != False
            purchase_team_not = self.partner_id.purchase_partner_team_id != self.current_purchase_team_id and self.partner_id.current_purchase_team_id != False
            all_purchase_not = purchase_user_not and purchase_team_not
            
            all_user_not = sale_user_not and purchase_user_not
            all_team_not = sale_team_not and purchase_team_not
            all_not = all_user_not and all_team_not

            is_kyc = self.application_type == 'kyc'
            is_customer = self.application_type in ['crm','customer_credit','customer_strategy']
            is_vendor = self.application_type in ['vrm','vendor_credit','vendor_strategy']

            #raise UserError(str(sale_team_not) + ' - ' + str(self.partner_id.team_id) + ' - ' + str(self.current_sale_team_id))

            if self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs'):
                A = 1
            elif self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs'):
                if is_kyc:
                    if sale_team_not and purchase_team_not:
                        raise UserError("You do not have access to this record.")
                elif is_customer:
                    if sale_team_not:
                        raise UserError("You do not have access to this record.")
                elif is_vendor:
                    if purchase_team_not:
                        raise UserError("You do not have access to this record.")
            elif self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs'):
                if is_kyc:
                    if all_user_not and purchase_user_not:
                        raise UserError("You do not have access to this record.")
                elif is_customer:
                    if sale_user_not:
                        raise UserError("You do not have access to this record.")
                elif is_vendor:
                    if purchase_user_not:
                        raise UserError("You do not have access to this record.")
        
            #check application request type
            if self.application_request_type != 'new':
                if self.application_type == 'kyc' and not self.current_kyc_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'crm' and not self.current_crm_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'customer_credit' and not self.current_customer_credit_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'customer_strategy' and not self.current_customer_strategy_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'vrm' and not self.current_vrm_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'vendor_credit' and not self.current_vendor_credit_id:
                    raise UserError("No current Active application to review/amend")
                if self.application_type == 'vendor_strategy' and not self.current_vendor_strategy_id:
                    raise UserError("No current Active application to review/amend")
            elif self.application_request_type == 'new':
                if self.application_type == 'kyc' and self.current_kyc_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'crm' and self.current_crm_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'customer_credit' and self.current_customer_credit_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'customer_strategy' and self.current_customer_strategy_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'vrm' and self.current_vrm_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'vendor_credit' and self.current_vendor_credit_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                if self.application_type == 'vendor_strategy' and self.current_vendor_strategy_id:
                    raise UserError("There is an existing application, please choose to either Review or Amend")
                
   
    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        hide_list = [
            #'active',
            #'name',
            'color',
            #'company_id',
            #'currency_id',
            #'state',
            'current_user_id',
            'current_sale_team_id',
            'current_purchase_team_id',
            #'partner_id',
            'is_late_review',
            'is_admin',
            'current_kyc_id',
            'current_kyc_state',
            'current_kyc_expiry_date',
            'current_kyc_review_date',
            'current_crm_id',
            'current_crm_state',
            'current_crm_expiry_date',
            'current_crm_review_date',
            'current_vrm_id',
            'current_vrm_state',
            'current_vrm_expiry_date',
            'current_vrm_review_date',
            'current_customer_credit_id',
            'current_customer_credit_state',
            'current_customer_credit_expiry_date',
            'current_customer_credit_review_date',
            'current_vendor_credit_id',
            'current_vendor_credit_state',
            'current_vendor_credit_expiry_date',
            'current_vendor_credit_review_date',
            'current_customer_strategy_id',
            'current_customer_strategy_state',
            'current_customer_strategy_expiry_date',
            'current_customer_strategy_review_date',
            'current_vendor_strategy_id',
            'current_vendor_strategy_state',
            'current_vendor_strategy_expiry_date',
            'current_vendor_strategy_review_date',
            #'application_type',
            #'application_request_type',
            'expiry_date_formula',
            #'expiry_date',
            'review_date_formula',
            #'review_date',
            #'company_type',
            #'legal_name',
            #'name_alt_lang',
            #'trade_name',
            #'trade_name_alt_lang',
            #'category_id',
            #'street',
            #'street2',
            #'zip',
            #'city',
            #'state_id',
            #'country_id',
            #'country_code',
            #'l10n_sa_edi_building_number',
            #'l10n_sa_edi_plot_identification',
            #'email',
            #'phone',
            #'mobile',
            #'website',
            #'company_registry',
            #'company_registry_expiry_date',
            #'vat',
            #'ref',
            #'legal_type',
            #'industry_id',
            #'paidup_capital',
            #'ownership_structure',
            #'management_structure',
            #'year_founded',
            #'function',
            #'title',
            #'duplicate_approved',
            #'user_id',
            #'team_id',
            #'customer_class',
            #'customer_segment',
            #'customer_pricelist_ids',
            #'deal_min_margin',
            #'annual_revenues',
            #'employee_count',
            #'countries_covered',
            #'business_brief',
            #'account_requirements',
            #'major_countries',
            #'services_needed',
            #'service_categories_needed',
            #'operation_brief',
            #'account_kpis',
            #'client_projects',
            #'client_profile',
            #'client_history',
            #'stakeholders',
            #'whitespace',
            #'sales_performance',
            #'margin_performance',
            #'wins_losses',
            #'account_competitors',
            #'competitors_stregnths',
            #'competitors_weaknesses',
            #'buyer_journey',
            #'content_channels',
            #'evaluation_criteria',
            #'decision_criteria',
            #'relationship_current_status',
            #'relationship_target_status',
            #'core_business_partners',
            #'relationship_progression_strategy',
            #'services',
            #'sales_targets',
            #'cross_sell',
            #'risks_challenges',
            #'critical_resources',
            #'monthly_expected_business',
            #'customer_credit_limit',
            #'credit_trade_references',
            #'customer_payment_term_ids',
            #'buyer_id',
            #'purchase_team_id',
            #'vendor_class',
            #'vendor_segment',
            #'vendor_currency_ids',
            #'vendor_annual_revenues',
            #'vendor_employee_count',
            #'vendor_countries_covered',
            #'vendor_business_brief',
            #'vendor_account_offerings',
            #'vendor_major_countries',
            #'services_provided',
            #'service_categories_provided',
            #'vendor_operation_brief',
            #'vendor_kpis',
            #'vendor_projects',
            #'vendor_profile',
            #'vendor_history',
            #'vendor_stakeholders',
            #'vendor_whitespace',
            #'purchases_performance',
            #'vendor_wins_losses',
            #'vendor_competitors',
            #'vendor_competitors_stregnths',
            #'vendor_competitors_weaknesses',
            #'selling_journey',
            #'vendor_content_channels',
            #'vendor_evaluation_criteria',
            #'vendor_decision_criteria',
            #'vendor_relationship_current_status',
            #'vendor_relationship_target_status',
            #'vendor_core_business_partners',
            #'vendor_relationship_progression_strategy',
            #'vendor_services',
            #'purchases_targets',
            #'vendor_risks_challenges',
            #'vendor_critical_resources',
            #'vendor_monthly_expected_business',
            #'vendor_credit_limit',
            #'vendor_payment_term_ids',
            #'attachment_ids',
            #'user_action_ids',
            'previous_company_type',
            'previous_legal_name',
            'previous_name_alt_lang',
            'previous_trade_name',
            'previous_trade_name_alt_lang',
            'previous_category_id',
            'previous_street',
            'previous_street2',
            'previous_zip',
            'previous_city',
            'previous_state_id',
            'previous_country_id',
            'previous_country_code',
            'previous_l10n_sa_edi_building_number',
            'previous_l10n_sa_edi_plot_identification',
            'previous_email',
            'previous_phone',
            'previous_mobile',
            'previous_website',
            'previous_company_registry',
            'previous_company_registry_expiry_date',
            'previous_vat',
            'previous_ref',
            'previous_legal_type',
            'previous_industry_id',
            'previous_paidup_capital',
            'previous_ownership_structure',
            'previous_management_structure',
            'previous_year_founded',
            'previous_function',
            'previous_title',
            'previous_duplicate_approved',
            'previous_user_id',
            'previous_team_id',
            'previous_customer_class',
            'previous_customer_segment',
            'previous_customer_pricelist_ids',
            'previous_deal_min_margin',
            'previous_annual_revenues',
            'previous_employee_count',
            'previous_countries_covered',
            'previous_business_brief',
            'previous_account_requirements',
            'previous_major_countries',
            'previous_services_needed',
            'previous_service_categories_needed',
            'previous_operation_brief',
            'previous_monthly_expected_business',
            'previous_customer_credit_limit',
            'previous_credit_trade_references',
            'previous_customer_payment_term_ids',
            'previous_account_kpis',
            'previous_client_projects',
            'previous_client_profile',
            'previous_client_history',
            'previous_stakeholders',
            'previous_whitespace',
            'previous_sales_performance',
            'previous_margin_performance',
            'previous_wins_losses',
            'previous_account_competitors',
            'previous_competitors_stregnths',
            'previous_competitors_weaknesses',
            'previous_buyer_journey',
            'previous_content_channels',
            'previous_evaluation_criteria',
            'previous_decision_criteria',
            'previous_relationship_current_status',
            'previous_relationship_target_status',
            'previous_core_business_partners',
            'previous_relationship_progression_strategy',
            'previous_services',
            'previous_sales_targets',
            'previous_cross_sell',
            'previous_risks_challenges',
            'previous_critical_resources',
            'previous_buyer_id',
            'previous_purchase_team_id',
            'previous_vendor_class',
            'previous_vendor_segment',
            'previous_vendor_currency_ids',
            'previous_vendor_annual_revenues',
            'previous_vendor_employee_count',
            'previous_vendor_countries_covered',
            'previous_vendor_business_brief',
            'previous_vendor_account_offerings',
            'previous_vendor_major_countries',
            'previous_services_provided',
            'previous_service_categories_provided',
            'previous_vendor_operation_brief',
            'previous_vendor_monthly_expected_business',
            'previous_vendor_credit_limit',
            'previous_vendor_payment_term_ids',
            'previous_vendor_kpis',
            'previous_vendor_projects',
            'previous_vendor_profile',
            'previous_vendor_history',
            'previous_vendor_stakeholders',
            'previous_vendor_whitespace',
            'previous_purchases_performance',
            'previous_vendor_wins_losses',
            'previous_vendor_competitors',
            'previous_vendor_competitors_stregnths',
            'previous_vendor_competitors_weaknesses',
            'previous_selling_journey',
            'previous_vendor_content_channels',
            'previous_vendor_evaluation_criteria',
            'previous_vendor_decision_criteria',
            'previous_vendor_relationship_current_status',
            'previous_vendor_relationship_target_status',
            'previous_vendor_core_business_partners',
            'previous_vendor_relationship_progression_strategy',
            'previous_vendor_services',
            'previous_purchases_targets',
            'previous_vendor_risks_challenges',
            'previous_vendor_critical_resources',
            'same_pa_vat_partner_id',
            'same_pa_company_registry_partner_id',
            'same_pa_name_partner_id',
            'same_pa_website_partner_id',
            'same_pa_email_partner_id',
            'same_pa_phone_partner_id',
            'same_pa_mobile_partner_id',
        ]
        for field in hide_list:
            if res.get(field):
                res[field]['searchable'] = False
                res[field]['selectable'] = False # to hide in Add Custom filter view
                res[field]['sortable'] = False # to hide in group by view
                res[field]['exportable'] = False # to hide in export list
                res[field]['store'] = False # to hide in 'Select Columns' filter in tree views

        return res



class ResPartnerApplicationAttachment(models.Model):
    _name = 'res.partner.application.attachment'
    _description = "Application Attachments"
    _order = 'create_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("Name")
    attachment_type_id = fields.Many2one('res.partner.application.attachment.type', string="Attachment Type")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    application_id = fields.Many2one('res.partner.application', string="Application")

class ResPartnerApplicationAttachmentTypes(models.Model):
    _name = 'res.partner.application.attachment.type'
    _description = "Application Attachment Types"
    _order = 'sequence, id desc'
    
    sequence = fields.Integer("Sequence")
    name = fields.Char("Name")

class ResPartnerApplicationUserAction(models.Model):
    _name = 'res.partner.application.user.action'
    _description = "Application User Actions"
    
    user_id = fields.Many2one('res.users', string='User', no_sort=True)
    action = fields.Selection([('created','Created'),('submitted','Submitted'),('resubmitted','Re-Submitted'),('validated','Validated'),('returned','Returned'),('approved','Approved'),('activated','Activated'),('rejected','Rejected'),('pending_validation','Pending Validation'),('pending_approval','Pending Approval'),('validated_by_others','Validated by Others'),('approved_by_others','Approved by Others'),('rejected_by_others','Rejected by Others'),('returned_by_others','Returned by Others'),('cancelled','Cancelled'),('cancelled_by_others','Cancelled by Others'),('expired','Expired')], string="Action", no_sort=True)
    action_datetime = fields.Datetime(string="Timestamp", default=fields.Datetime.now(), no_sort=True)
    pending_timestamp = fields.Datetime(string="Pending Timestamp", no_sort=True)
    pending_time = fields.Float(string="Pending Hours", compute="_compute_pending_time", no_sort=True)
    application_id = fields.Many2one('res.partner.application', string="Application", no_sort=True)
    note = fields.Text(string="Notes")

    @api.depends('action_datetime','pending_timestamp')
    def _compute_pending_time(self):
        for record in self:
            record.pending_time = False
            if record.pending_timestamp:
                record.pending_time = (record.action_datetime - record.pending_timestamp).total_seconds() / 60 / 60

    