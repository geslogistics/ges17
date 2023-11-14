# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    """
    #current kyc fields
    
    kyc_company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], store=True, related="current_kyc_id.company_type")
    kyc_legal_name = fields.Char(string='English Official Name', store=True, related="current_kyc_id.legal_name")
    kyc_arabic_name = fields.Char(string='Arabic Name', store=True, related="current_kyc_id.arabic_name")
    kyc_trade_name = fields.Char(string='Trading Name', store=True, related="current_kyc_id.trade_name")

    kyc_category_id = fields.Many2many('res.partner.category', 'partner_tags_kyc_application', 'application_partner_id' ,'application_category_id', string='Tags', store=True, related="current_kyc_id.category_id")
    kyc_street = fields.Char(string="Street", store=True, related="current_kyc_id.street")
    kyc_street2 = fields.Char(string="Street 2", store=True, related="current_kyc_id.street2")
    kyc_zip = fields.Char(string="Zip", store=True, related="current_kyc_id.zip")
    kyc_city = fields.Char(string="City", store=True, related="current_kyc_id.city")
    kyc_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]", store=True, related="current_kyc_id.state_id")
    kyc_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', store=True, related="current_kyc_id.country_id")

    kyc_email = fields.Char(string="Email", store=True, related="current_kyc_id.email")
    kyc_phone = fields.Char(string="Phone", store=True, related="current_kyc_id.phone")
    kyc_mobile = fields.Char(string="Mobile", store=True, related="current_kyc_id.mobile")
    kyc_website = fields.Char(string="Website", store=True, related="current_kyc_id.website")
    kyc_company_registry = fields.Char(string="Official ID", store=True, related="current_kyc_id.company_registry")
    kyc_vat = fields.Char(string='Tax ID', store=True, related="current_kyc_id.vat")
    kyc_ref = fields.Char(string='Reference', store=True, related="current_kyc_id.ref")


    ## KYC - Companies
    kyc_legal_type = fields.Selection([('establishment','Establishment'),('joint_liability','Joint Liability Company'),('limited_partnership','Limited Partnership Company'),('simple_joint','Simple Joint Stock Company'),('closed_joint','Closed Joint Stock Company'),('public','Public Joint Stock Company'),('llc','Limited Liability Company'),('one_llc','One Person Limited Liability Company')], string="Legal Type", store=True, related="current_kyc_id.legal_type")
    kyc_industry_id = fields.Many2one('res.partner.industry', string="Industry", store=True, related="current_kyc_id.industry_id")
    kyc_paidup_capital = fields.Monetary("Paid-up Capital", store=True, related="current_kyc_id.paidup_capital")
    kyc_ownership_structure = fields.Html("Ownership Structure", store=True, related="current_kyc_id.ownership_structure")
    kyc_management_structure = fields.Html("Management Structure", store=True, related="current_kyc_id.management_structure")
    kyc_year_founded = fields.Integer("Year Founded", store=True, related="current_kyc_id.year_founded")
    

    ## KYC - Individuals
    kyc_function = fields.Char("Job Position", store=True, related="current_kyc_id.function")
    kyc_title = fields.Many2one('res.partner.title', string="Title", store=True, related="current_kyc_id.title")

    """

    application_ids = fields.One2many('res.partner.application','partner_id', string="Applications")
    active_application_ids = fields.Many2many('res.partner.application', 'partner_tags_active_application', 'application_partner_id' ,'application_category_id', string='Active Applications')

    is_locked = fields.Boolean(string="Locked", tracking=True, compute_sudo=True, compute="_lock_partner")

    @api.depends('current_kyc_id','current_crm_id','current_customer_credit_id','current_customer_strategy_id','current_vrm_id','current_vendor_credit_id','current_vendor_strategy_id')
    def _lock_partner(self):
        for record in self:
            if record.current_kyc_id:
                record.is_locked = True
            else:
                record.is_locked = False
    """
    @api.depends('current_kyc_id','current_crm_id','current_customer_credit_id','current_customer_strategy_id','current_vrm_id','current_vendor_credit_id','current_vendor_strategy_id')
    def _get_active_applications(self):
        for record in self:
            #record.active_application_ids = self.env['res.partner.application'].sudo().search([('id','=','1')])
            record.active_application_ids = record.current_kyc_id + record.current_crm_id  + record.current_customer_credit_id  + record.current_customer_strategy_id  + record.current_vrm_id  + record.current_vendor_credit_id + record.current_vendor_strategy_id
    """

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

    """
    @api.onchange('current_kyc_id')
    def _update_partner_kyc_fields(self):
        for record in self:
            record.company_type = record.current_kyc_id.company_type
            record.street = record.current_kyc_id.street
            record.street2 = record.current_kyc_id.street2
            record.city = record.current_kyc_id.city
            record.state_id = record.current_kyc_id.state_id.id
            record.zip = record.current_kyc_id.zip
            record.country_id = record.current_kyc_id.country_id.id
            #record.l10n_sa_edi_building_number = record.current_kyc_id.l10n_sa_edi_building_number
            #record.l10n_sa_edi_plot_identification = record.current_kyc_id.l10n_sa_edi_plot_identification
            #record.is_customer = True if record.current_kyc_id.application_direction == 'customer' else record.is_vendor
            #record.is_vendor = True if record.current_kyc_id.application_direction == 'vendor' else record.is_vendor       
            record.name = record.current_kyc_id.legal_name
            record.trade_name = record.current_kyc_id.trade_name
            record.arabic_name = record.current_kyc_id.arabic_name
            record.category_id = record.current_kyc_id.category_id.ids
            record.company_registry = record.current_kyc_id.company_registry
            record.vat = record.current_kyc_id.vat
            record.ref = record.current_kyc_id.ref
            record.legal_type = record.current_kyc_id.legal_type
            record.industry_id = record.current_kyc_id.industry_id.id
            record.paidup_capital = record.current_kyc_id.paidup_capital
            record.ownership_structure = record.current_kyc_id.ownership_structure
            record.management_structure = record.current_kyc_id.management_structure
            record.year_founded = record.current_kyc_id.year_founded
            record.function = record.current_kyc_id.function
            record.title = record.current_kyc_id.title
    """     
            
          


    """
    def action_validate(self):
        for rec in self:
            rec.write({'state': 'validated'})

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def action_activate(self):
        for rec in self:
            rec.write({'state': 'active'})

    def action_hold(self):
        for rec in self:
            rec.write({'state': 'hold'})

    def action_exception(self):
        for rec in self:
            rec.write({'state': 'exception'})

    def action_blacklist(self):
        for rec in self:
            rec.write({'state': 'blacklist'})

    def action_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def write(self, values):
        if 'state' in values:
            new_state = values.get('state')
            if new_state == 'approved' or self.state == 'approved':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_approval'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            if new_state == 'validated' or self.state == 'draft':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_validation'):
                    raise ValidationError(
                        _("Only Managers can perform that move!"))
            if new_state == 'active' or self.state == 'active':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_activate'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            if new_state == 'hold' or self.state == 'hold':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_hold'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            if new_state == 'exception' or self.state == 'exception':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_exception'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            if new_state == 'blacklist' or self.state == 'blacklist':
                if not self.env.user.has_group(
                        'ges_logistics_partner.'
                        'ges_logistics_partner_group_blacklist'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
        return super().write(values)
    """
