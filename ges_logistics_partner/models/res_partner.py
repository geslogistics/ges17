# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    is_pa_user = fields.Boolean(string="Is PA User", compute="_compute_is_pa_user", store=False)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs')
    

    # teams inherits
    pa_user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user.id,
        )

    pa_team_id = fields.Many2one(
        'crm.team',
        string="Sales Team",
        related="pa_user_id.sale_team_id"
        )

    pa_buyer_id = fields.Many2one(
        'res.users', 
        string="Buyer", 
        default=lambda self: self.env.user.id,
        )
    
    purchase_partner_team_id = fields.Many2one(
        'purchase.team',
        string="Purchase Team",
        related="pa_buyer_id.purchase_team_id"
        )

    #application inherits
    
    application_ids = fields.One2many('res.partner.application','partner_id', string="Applications")
    active_application_ids = fields.Many2many('res.partner.application', 'partner_tags_active_application', 'application_partner_id' ,'application_category_id', string='Active Applications')

    is_locked = fields.Boolean(string="Locked", tracking=True, compute_sudo=True, compute="_lock_partner")

    pa_property_product_pricelist = fields.Many2one(
        'product.pricelist',
        string="Pricelist",
        store=True,
        ondelete='restrict',
        )
    
    pa_domain_property_product_pricelist = fields.Char(
        compute="_compute_pa_property_product_pricelist_domain",
        readonly=True,
        store=False,
        )

    pa_property_payment_term_id = fields.Many2one(
        'account.payment.term',
        string="Payment Terms",
        store=True,
        ondelete='restrict',
        )
                
    pa_domain_property_payment_term_id = fields.Char(
       compute="_compute_pa_property_payment_term_id_domain",
       readonly=True,
       store=False,
       )

    pa_property_purchase_currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        store=True,
        ondelete='restrict',
        )
    
    pa_domain_property_purchase_currency_id = fields.Char(
        compute="_compute_pa_property_purchase_currency_id_domain",
        readonly=True,
        store=False,
        )

    pa_property_supplier_payment_term_id = fields.Many2one(
        'account.payment.term',
        string="Payment Terms",
        store=True,
        ondelete='restrict',
        )
                
    pa_domain_property_supplier_payment_term_id = fields.Char(
       compute="_compute_pa_property_supplier_payment_term_id_domain",
       readonly=True,
       store=False,
       )

    @api.onchange('current_crm_id.customer_pricelist_ids')
    @api.depends('current_crm_id.customer_pricelist_ids')
    def _compute_pa_property_product_pricelist_domain(self):
        for record in self.sudo():
            current_pa_pricelist_ids = record.current_crm_id.customer_pricelist_ids.ids
            if current_pa_pricelist_ids:
                record.pa_domain_property_product_pricelist = json.dumps(
                [('id','in',current_pa_pricelist_ids), ('company_id', 'in', (False, record.company_id.id))]
                )
            else:
                record.pa_domain_property_product_pricelist = json.dumps(
                [('company_id', 'in', (False, record.company_id.id))]
                )

    @api.onchange('current_customer_credit_id.customer_payment_term_ids')
    @api.depends('current_customer_credit_id.customer_payment_term_ids')
    def _compute_pa_property_payment_term_id_domain(self):
        for record in self.sudo():
            cash_days = 0
            current_pa_payment_term_ids = record.current_customer_credit_id.customer_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_pa_payment_term_ids:
                record.pa_domain_property_payment_term_id = json.dumps(
                ['|',('id','in',current_pa_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.pa_domain_property_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    @api.onchange('current_vrm_id.vendor_currency_ids')
    @api.depends('current_vrm_id.vendor_currency_ids')
    def _compute_pa_property_purchase_currency_id_domain(self):
        for record in self.sudo():
            current_pa_currency_ids = record.current_vrm_id.vendor_currency_ids.ids
            if current_pa_currency_ids:
                record.pa_domain_property_purchase_currency_id = json.dumps(
                [('id','in',current_pa_currency_ids)]
                )
            else:
                record.pa_domain_property_purchase_currency_id = []

    @api.onchange('current_vendor_credit_id.vendor_payment_term_ids')
    @api.depends('current_vendor_credit_id.vendor_payment_term_ids')
    def _compute_pa_property_supplier_payment_term_id_domain(self):
        for record in self.sudo():
            cash_days = 0
            current_pa_payment_term_ids = record.current_vendor_credit_id.vendor_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_pa_payment_term_ids:
                record.pa_domain_property_supplier_payment_term_id = json.dumps(
                ['|',('id','in',current_pa_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.pa_domain_property_supplier_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    @api.depends('pa_pricelist_id')
    @api.onchange('pa_pricelist_id')
    def update_pricelist_id_to_pa_field(self):
        self.property_product_pricelist = self.pa_pricelist_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_payment_term_id_to_pa_field(self):
        self.property_payment_term_id = self.pa_payment_term_id.id

    @api.depends('pa_user_id')
    @api.onchange('pa_user_id')
    def update_user_id_to_pa_field(self):
        self.user_id = self.pa_user_id.id

    @api.depends('pa_team_id')
    @api.onchange('pa_team_id')
    def update_team_id_to_pa_field(self):
        self.team_id = self.pa_team_id.id

    @api.depends('pa_buyer_id')
    @api.onchange('pa_buyer_id')
    def update_buyer_id_to_pa_field(self):
        self.buyer_id = self.pa_buyer_id.id

    @api.depends('pa_vendor_currency_id')
    @api.onchange('pa_vendor_currency_id')
    def update_vendor_currency_id_to_pa_field(self):
        self.property_purchase_currency_id = self.pa_vendor_currency_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_vendor_payment_term_id_to_pa_field(self):
        self.property_supplier_payment_term_id = self.pa_payment_term_id.id

    

    @api.depends('current_kyc_id','current_crm_id','current_customer_credit_id','current_customer_strategy_id','current_vrm_id','current_vendor_credit_id','current_vendor_strategy_id')
    def _lock_partner(self):
        for record in self:
            if record.current_kyc_id:
                record.is_locked = True
            else:
                record.is_locked = False
    
    def write(self, vals):

        #kyc fields update
        if (vals.get('current_kyc_id') or self.current_kyc_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'company_type',
                'name',
                'category_id',
                'street',
                'street2',
                'zip',
                'city',
                'state_id',
                'country_id',
                'email',
                'phone',
                'mobile',
                'website',
                'company_registry',
                'vat',
                'ref',
                'industry_id',
                'function',
                'title',
                ]
            if any(x in list_of_fields for x in vals.keys()):
                raise UserError("File is locked. Changes must be through KYC Applications")

        #crm fields update
        if (vals.get('current_crm_id') or self.current_crm_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'user_id',
                'team_id',
                ]
            if any(x in list_of_fields for x in vals.keys()):
                raise UserError("File is locked. Changes must be through CRM Applications")

        #vrm fields update
        if (vals.get('current_vrm_id') or self.current_vrm_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'buyer_id',
                'purchase_partner_team_id',
                ]
            if any(x in list_of_fields for x in vals.keys()):
                raise UserError("File is locked. Changes must be through VRM Applications")
        
        
        return super(ResPartner, self).write(vals)


    #Application fields
    current_kyc_id = fields.Many2one('res.partner.application', string="KYC Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','kyc'),('state','=','active')]")
    current_kyc_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='KYC Status', related="current_kyc_id.state")
    current_kyc_late_review = fields.Boolean(string="KYC Late", related="current_kyc_id.is_late_review")
    current_kyc_expiry_date = fields.Date(string="KYC Expiry Date", related="current_kyc_id.expiry_date")
    current_kyc_review_date = fields.Date(string="KYC Review Date", related="current_kyc_id.review_date")

    current_crm_id = fields.Many2one('res.partner.application', string="CRM Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','crm'),('state','=','active')]")
    current_crm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='CRM Status', related="current_crm_id.state")
    current_crm_late_review = fields.Boolean(string="CRM Late", related="current_crm_id.is_late_review")
    current_crm_expiry_date = fields.Date(string="CRM Expiry Date", related="current_crm_id.expiry_date")
    current_crm_review_date = fields.Date(string="CRM Review Date", related="current_crm_id.review_date")

    current_vrm_id = fields.Many2one('res.partner.application', string="VRM Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','vrm'),('state','=','active')]")
    current_vrm_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='VRM Status', related="current_vrm_id.state")
    current_vrm_late_review = fields.Boolean(string="VRM Late", related="current_vrm_id.is_late_review")
    current_vrm_expiry_date = fields.Date(string="VRM Expiry Date", related="current_vrm_id.expiry_date")
    current_vrm_review_date = fields.Date(string="VRM Review Date", related="current_vrm_id.review_date")

    current_customer_credit_id = fields.Many2one('res.partner.application', string="Customer Credit Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','customer_credit'),('state','=','active')]")
    current_customer_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Credit Status', related="current_customer_credit_id.state")
    current_customer_credit_late_review = fields.Boolean(string="Customer Credit Late", related="current_customer_credit_id.is_late_review")
    current_customer_credit_expiry_date = fields.Date(string="Customer Credit Expiry Date", related="current_customer_credit_id.expiry_date")
    current_customer_credit_review_date = fields.Date(string="Customer Credit Review Date", related="current_customer_credit_id.review_date")

    current_vendor_credit_id = fields.Many2one('res.partner.application', string="Vendor Credit Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','vendor_credit'),('state','=','active')]")
    current_vendor_credit_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Credit Status', related="current_vendor_credit_id.state")
    current_vendor_credit_late_review = fields.Boolean(string="Vendor Credit Late", related="current_vendor_credit_id.is_late_review")
    current_vendor_credit_expiry_date = fields.Date(string="Vendor Credit Expiry Date", related="current_vendor_credit_id.expiry_date")
    current_vendor_credit_review_date = fields.Date(string="Vendor Credit Review Date", related="current_vendor_credit_id.review_date")

    current_customer_strategy_id = fields.Many2one('res.partner.application', string="Customer Strategy Credit Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','customer_strategy'),('state','=','active')]")
    current_customer_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Customer Strategy Status', related="current_customer_strategy_id.state")
    current_customer_strategy_late_review = fields.Boolean(string="Customer Strategy Late", related="current_customer_strategy_id.is_late_review")
    current_customer_strategy_expiry_date = fields.Date(string="Customer Strategy Expiry Date", related="current_customer_strategy_id.expiry_date")
    current_customer_strategy_review_date = fields.Date(string="Customer Strategy Review Date", related="current_customer_strategy_id.review_date")
    
    current_vendor_strategy_id = fields.Many2one('res.partner.application', string="Vendor Strategy Credit Application", tracking=True, domain="[('partner_id', '=', id),('application_type','=','vendor_strategy'),('state','=','active')]")
    current_vendor_strategy_state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('approved', 'Approved'),('active', 'Active'),('hold', 'Hold'),('cancel', 'Cancelled')], string='Vendor Strategy Status', related="current_vendor_strategy_id.state")
    current_vendor_strategy_late_review = fields.Boolean(string="Vendor Strategy Late", related="current_vendor_strategy_id.is_late_review")
    current_vendor_strategy_expiry_date = fields.Date(string="Vendor Strategy Expiry Date", related="current_vendor_strategy_id.expiry_date")
    current_vendor_strategy_review_date = fields.Date(string="Vendor Strategy Review Date", related="current_vendor_strategy_id.review_date")



class ResUser(models.Model):
    _inherit = 'res.users'

    #application inherits
    
    purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")
