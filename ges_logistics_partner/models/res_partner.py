# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    current_sale_team_id = fields.Many2one('crm.team', string='Sales Team', related="current_user_id.sale_team_id")
    current_purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team', related="current_user_id.purchase_team_id")
    is_pa_user = fields.Boolean(string="Is PA User", compute="_compute_is_pa_user", store=False)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs')
    
    #duplicate approval
    duplicate_approved = fields.Boolean('Duplicate Partner', default=False)
    
    # general partner account number

    account_number = fields.Char(string="Account Number")

    # teams inherits
    pa_user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user.id,
        )

    pa_team_id = fields.Many2one(
        'crm.team',
        string="Sales Team",
        related="pa_user_id.sale_team_id",
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
                [('id','in',current_pa_pricelist_ids), ('company_id', 'in', (False, self.env.company.id))]
                )
            else:
                record.pa_domain_property_product_pricelist = json.dumps(
                [('company_id', 'in', (False, self.env.company.id))]
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
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, self.env.company.id))]
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
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, self.env.company.id))]
                )

    # update pa fields

    @api.depends('pa_property_product_pricelist')
    @api.onchange('pa_property_product_pricelist')
    def update_property_product_pricelist_to_pa_field(self):
        if self.is_pa_user:
            self.property_product_pricelist = self.pa_property_product_pricelist.id

    @api.depends('pa_property_payment_term_id')
    @api.onchange('pa_property_payment_term_id')
    def update_property_payment_term_id_to_pa_field(self):
        if self.is_pa_user:
            self.property_payment_term_id = self.pa_property_payment_term_id.id

    @api.depends('pa_user_id')
    @api.onchange('pa_user_id')
    def update_user_id_to_pa_field(self):
        if self.is_pa_user:
            self.user_id = self.pa_user_id.id

    @api.depends('pa_team_id')
    @api.onchange('pa_team_id')
    def update_team_id_to_pa_field(self):
        if self.is_pa_user:
            self.team_id = self.pa_team_id.id

    @api.depends('pa_property_purchase_currency_id')
    @api.onchange('pa_property_purchase_currency_id')
    def update_property_purchase_currency_id_to_pa_field(self):
        if self.is_pa_user:
            self.property_purchase_currency_id = self.pa_property_purchase_currency_id.id

    @api.depends('pa_property_supplier_payment_term_id')
    @api.onchange('pa_property_supplier_payment_term_id')
    def update_property_supplier_payment_term_id_to_pa_field(self):
        if self.is_pa_user:
            self.property_supplier_payment_term_id = self.pa_property_supplier_payment_term_id.id

    @api.depends('pa_buyer_id')
    @api.onchange('pa_buyer_id')
    def update_buyer_id_to_pa_field(self):
        if self.is_pa_user:
            self.buyer_id = self.pa_buyer_id.id

    

    #reverse update pa fields
    @api.depends('property_product_pricelist')
    @api.onchange('property_product_pricelist')
    def update_pa_property_product_pricelist_to_field(self):
        if not self.is_pa_user:
            self.pa_property_product_pricelist = self.property_product_pricelist.id

    @api.depends('property_payment_term_id')
    @api.onchange('property_payment_term_id')
    def update_pa_property_payment_term_id_to_field(self):
        if not self.is_pa_user:
            self.pa_property_payment_term_id = self.property_payment_term_id.id

    @api.depends('user_id')
    @api.onchange('user_id')
    def update_pa_user_id_to_field(self):
        if not self.is_pa_user:
            self.pa_user_id = self.user_id.id

    @api.depends('team_id')
    @api.onchange('team_id')
    def update_pa_team_id_to_field(self):
        if not self.is_pa_user:
            self.pa_team_id = self.team_id.id

    @api.depends('buyer_id')
    @api.onchange('buyer_id')
    def update_pa_buyer_id_to_field(self):
        if not self.is_pa_user:
            self.pa_buyer_id = self.buyer_id.id

    @api.depends('property_purchase_currency_id')
    @api.onchange('property_purchase_currency_id')
    def update_pa_property_purchase_currency_id_to_field(self):
        if not self.is_pa_user:
            self.pa_property_purchase_currency_id = self.property_purchase_currency_id.id

    @api.depends('property_supplier_payment_term_id')
    @api.onchange('property_supplier_payment_term_id')
    def update_pa_property_supplier_payment_term_id_to_field(self):
        if not self.is_pa_user:
            self.pa_property_supplier_payment_term_id = self.property_supplier_payment_term_id.id
    
    @api.model
    def create(self, values):
        values['account_number'] = self.env['ir.sequence'].next_by_code('res.partner.uniqseq')
            
        result = super(ResPartner, self).create(values)
        
        return result
    
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
                'duplicate_approved',
                ]
            if any(x in list_of_fields for x in vals.keys()) and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin'):
                raise UserError("File is locked. Changes must be through KYC Applications")

        #crm fields update
        if (vals.get('current_crm_id') or self.current_crm_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'user_id',
                'team_id',
                ]
            if any(x in list_of_fields for x in vals.keys()) and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin'):
                raise UserError("File is locked. Changes must be through CRM Applications")

        #customer_credit fields update
        if (vals.get('current_customer_credit_id') or self.current_customer_credit_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'property_payment_term_id',
                ]
            if any(x in list_of_fields for x in vals.keys()) and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin'):
                raise UserError("File is locked. Changes must be through CC Applications")

        #vrm fields update
        if (vals.get('current_vrm_id') or self.current_vrm_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'buyer_id',
                'purchase_partner_team_id',
                ]
            if any(x in list_of_fields for x in vals.keys()) and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin'):
                raise UserError("File is locked. Changes must be through VRM Applications")

        #vendor_credit fields update
        if (vals.get('current_vendor_credit_id') or self.current_vendor_credit_id) and self._context.get('through_partner_application') != True:
            list_of_fields = [
                'property_supplier_payment_term_id',
                ]
            if any(x in list_of_fields for x in vals.keys()) and not self.env.user.has_group('ges_logistics_partner.group_partner_application_admin'):
                raise UserError("File is locked. Changes must be through VC Applications")
        
        
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


    ####check duplication fields
    same_pa_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID', compute='_compute_same_pa_partner_id', store=False)
    same_pa_company_registry_partner_id = fields.Many2one('res.partner', string='Partner with same Company Registry', compute='_compute_same_pa_partner_id', store=False)
    same_pa_name_partner_id = fields.Many2one('res.partner', string='Partner with same Name', compute='_compute_same_pa_partner_id', store=False)
    same_pa_website_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_email_partner_id = fields.Many2one('res.partner', string='Partner with same Website', compute='_compute_same_pa_partner_id', store=False)
    same_pa_phone_partner_id = fields.Many2one('res.partner', string='Partner with same Phone', compute='_compute_same_pa_partner_id', store=False)
    same_pa_mobile_partner_id = fields.Many2one('res.partner', string='Partner with same Mobile', compute='_compute_same_pa_partner_id', store=False)
    

    @api.depends('vat', 'company_id', 'company_registry', 'country_id', 'name','website','email','phone','mobile')
    #@api.onchange('vat', 'company_id', 'company_registry', 'country_id', 'name','website','email','phone','mobile')
    def _compute_same_pa_partner_id(self):
        for partner in self.sudo():
            partner.same_pa_vat_partner_id = False
            partner.same_pa_company_registry_partner_id = False
            partner.same_pa_name_partner_id = False
            partner.same_pa_website_partner_id = False
            partner.same_pa_email_partner_id = False
            partner.same_pa_phone_partner_id = False
            partner.same_pa_mobile_partner_id = False

            if not partner.duplicate_approved:
                # use _origin to deal with onchange()
                partner_id = partner._origin.id
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
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
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
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
                partner.same_pa_company_registry_partner_id = bool(partner.company_registry) and Partner.search(domain, limit=1)

           

                # check name
                domain = [
                    ('name', 'ilike', partner.name),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
                partner.same_pa_name_partner_id = bool(partner.name) and Partner.search(domain, limit=1)

                # check website
                domain = [
                    ('website', '=', partner.website),
                    ('country_id','=',partner.country_id.id),
                    ('company_id', 'in', [False, partner.company_id.id]),
                    #('duplicate_approved', '=', False), 
                ]
                if partner_id:
                    domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
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
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
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
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
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
                if partner.parent_id:
                    domain += [('id', '!=', partner.parent_id.id), ('parent_id','!=',partner.parent_id.id)]
                partner.same_pa_mobile_partner_id = bool(partner.mobile) and Partner.search(domain, limit=1)

    def initiate_partner_application(self):

        context = {
            'default_partner_id': self.id,
            'default_application_type': self.env.context.get('crm_app_type'),
            'default_application_request_type': self.env.context.get('crm_app_state'),
        }

        return {
                #'name': name,
                'view_mode': 'form',
                'res_model': 'res.partner.application',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': context,
            }
        
        """
        if self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs'):
            return new_pa_win_act
        elif self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs'):
            if self.team_id == self.current_sale_team_id and self.team_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'crm' or self.env.context.get('crm_app_type') == 'customer_credit' or self.env.context.get('crm_app_type') == 'customer_strategy'):
                return new_pa_win_act
            elif self.purchase_partner_team_id == self.current_purchase_team_id and self.current_purchase_team_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'vrm' or self.env.context.get('crm_app_type') == 'vendor_credit' or self.env.context.get('crm_app_type') == 'vendor_strategy'):
                return new_pa_win_act
            elif self.user_id == self.current_user_id and self.user_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'crm' or self.env.context.get('crm_app_type') == 'customer_credit' or self.env.context.get('crm_app_type') == 'customer_strategy'):
                return new_pa_win_act
            elif self.buyer_id == self.current_user_id and self.buyer_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'vrm' or self.env.context.get('crm_app_type') == 'vendor_credit' or self.env.context.get('crm_app_type') == 'vendor_strategy'):
                return new_pa_win_act
            else:
                raise UserError("You do not have access to this record.")
        elif self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs'):
            if self.user_id == self.current_user_id and self.user_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'crm' or self.env.context.get('crm_app_type') == 'customer_credit' or self.env.context.get('crm_app_type') == 'customer_strategy'):
                return new_pa_win_act
            elif self.buyer_id == self.current_user_id and self.buyer_id != False and (self.env.context.get('crm_app_type') == 'kyc' or self.env.context.get('crm_app_type') == 'vrm' or self.env.context.get('crm_app_type') == 'vendor_credit' or self.env.context.get('crm_app_type') == 'vendor_strategy'):
                return new_pa_win_act
            else:
                raise UserError("You do not have access to this record.")
        else:
            raise UserError("You do not have access to this record.")
        """

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        hide_list = [
            'current_user_id',
            'current_sale_team_id',
            'current_purchase_team_id',
            'is_pa_user',
            'duplicate_approved',
            #'account_number',
            'pa_user_id',
            'pa_team_id',
            'pa_buyer_id',
            'purchase_partner_team_id',
            'application_ids',
            'active_application_ids',
            'pa_property_product_pricelist',
            'pa_domain_property_product_pricelist',
            'pa_property_payment_term_id',
            'pa_domain_property_payment_term_id',
            'pa_property_purchase_currency_id',
            'pa_domain_property_purchase_currency_id',
            'pa_property_supplier_payment_term_id',
            'pa_domain_property_supplier_payment_term_id',
            'current_kyc_id',
            'current_kyc_state',
            'current_kyc_late_review',
            'current_kyc_expiry_date',
            'current_kyc_review_date',
            'current_crm_id',
            'current_crm_state',
            'current_crm_late_review',
            'current_crm_expiry_date',
            'current_crm_review_date',
            'current_vrm_id',
            'current_vrm_state',
            'current_vrm_late_review',
            'current_vrm_expiry_date',
            'current_vrm_review_date',
            'current_customer_credit_id',
            'current_customer_credit_state',
            'current_customer_credit_late_review',
            'current_customer_credit_expiry_date',
            'current_customer_credit_review_date',
            'current_vendor_credit_id',
            'current_vendor_credit_state',
            'current_vendor_credit_late_review',
            'current_vendor_credit_expiry_date',
            'current_vendor_credit_review_date',
            'current_customer_strategy_id',
            'current_customer_strategy_state',
            'current_customer_strategy_late_review',
            'current_customer_strategy_expiry_date',
            'current_customer_strategy_review_date',
            'current_vendor_strategy_id',
            'current_vendor_strategy_state',
            'current_vendor_strategy_late_review',
            'current_vendor_strategy_expiry_date',
            'current_vendor_strategy_review_date',
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




class ResUser(models.Model):
    _inherit = 'res.users'

    #application inherits
    
    purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")
