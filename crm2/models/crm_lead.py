# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json
from lxml import etree

class Lead(models.Model):
    _inherit = 'crm.lead'


    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
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




    #lead fields
    contact_partner_id = fields.Many2one('res.partner', string='Contact Person', check_company=True, index=True, tracking=10)
    contact_email = fields.Char('Email', related="contact_partner_id.email")
    contact_mobile = fields.Char('Mobile', related="contact_partner_id.mobile")
    contact_phone = fields.Char('Email', related="contact_partner_id.phone")
    can_quote = fields.Boolean('can_quote', related="stage_id.can_quote")

    partner_type = fields.Selection([('customer','Customer'),('vendor','Vendor')], default='customer', string="Partner Type")

    @api.depends('partner_id','contact_partner_id')
    @api.onchange('partner_id','contact_partner_id')
    def update_names(self):
        for record in self:
            record.partner_name = record.partner_id.name
            record.contact_name = record.contact_partner_id.name

    referral_user_id = fields.Many2one('res.users', string='Referral User', default=lambda self: self.env.user)
    referral_ou_id = fields.Many2one('operating.unit', string='Referral Unit', compute='_compute_referral_ou', store=True)
    
    @api.depends('partner_type','referral_user_id')
    def _compute_referral_ou(self):
        for record in self:
            if record.partner_type == 'customer':
                record.referral_ou_id = record.referral_user_id.default_operating_unit_sales_id
            elif record.partner_type == 'vendor':
                record.referral_ou_id = record.referral_user_id.default_operating_unit_procurement_id

    sales_user_id = fields.Many2one('res.users', string='Sales User', related="partner_id.sales_user_id")
    sales_ou_id = fields.Many2one('operating.unit', string='Sales Unit', related="partner_id.sales_ou_id")

    procurement_user_id = fields.Many2one('res.users', string='Procurement User', related="partner_id.procurement_user_id")
    procurement_ou_id = fields.Many2one('operating.unit', string='Procurement Unit', related="partner_id.procurement_ou_id")
    
    assigned_user_id = fields.Many2one('res.users', string='Assigned User', compute='_compute_assigned_user_ou', store=True)
    assigned_ou_id = fields.Many2one('operating.unit', string='Assigned Unit', compute='_compute_assigned_user_ou', store=True)
    
    @api.depends('partner_type','sales_user_id','sales_ou_id','procurement_user_id','procurement_ou_id')
    def _compute_assigned_user_ou(self):
        for record in self:
            if record.partner_type == 'customer':
                if record.sales_user_id:
                    record.assigned_user_id = record.sales_user_id
                    record.assigned_ou_id = record.sales_ou_id
                else:
                    record.assigned_user_id = record.referral_user_id
                    record.assigned_ou_id = record.referral_ou_id
            elif record.partner_type == 'vendor':
                if record.procurement_user_id:
                    record.assigned_user_id = record.procurement_user_id
                    record.assigned_ou_id = record.procurement_ou_id
                else:
                    record.assigned_user_id = record.referral_user_id
                    record.assigned_ou_id = record.referral_ou_id

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



    ## stage pa checklist fields
    requires_kyc = fields.Boolean(string="KYC", related="stage_id.requires_kyc")
    requires_crm = fields.Boolean(string="CRM", related="stage_id.requires_crm")
    requires_cc = fields.Boolean(string="CC", related="stage_id.requires_cc")
    requires_cs = fields.Boolean(string="CS", related="stage_id.requires_cs")
    requires_vrm = fields.Boolean(string="VRM", related="stage_id.requires_vrm")
    requires_vc = fields.Boolean(string="VC", related="stage_id.requires_vc")
    requires_vs = fields.Boolean(string="VS", related="stage_id.requires_vs")


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

        
        return super(Lead, self).write(values)