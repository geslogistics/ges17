# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #application inherits
    
    application_ids = fields.One2many('res.partner.application','partner_id', string="Applications")
    active_application_ids = fields.Many2many('res.partner.application', 'partner_tags_active_application', 'application_partner_id' ,'application_category_id', string='Active Applications')

    is_locked = fields.Boolean(string="Locked", tracking=True, compute_sudo=True, compute="_lock_partner")

    domain_pricelist_id = fields.Char(
       compute="_compute_pricelist_id_domain",
       compute_sudo=True,
       readonly=True,
       store=False,
    )

    @api.onchange('current_crm_id.customer_pricelist_ids')
    @api.depends('current_crm_id.customer_pricelist_ids')
    def _compute_pricelist_id_domain(self):
        for record in self:
            current_pricelist_ids = record.current_crm_id.customer_pricelist_ids.ids
            if current_pricelist_ids:
                record.domain_pricelist_id = json.dumps(
                [('id','in',current_pricelist_ids), ('company_id', 'in', (False, record.company_id.id))]
                )
            else:
                record.domain_pricelist_id = json.dumps(
                [('company_id', 'in', (False, record.company_id.id))]
                )
                
    domain_payment_term_id = fields.Char(
       compute="_compute_payment_term_id_domain",
       compute_sudo=True,
       readonly=True,
       store=False,
    )

    @api.onchange('current_customer_credit_id.customer_payment_term_ids')
    @api.depends('current_customer_credit_id.customer_payment_term_ids')
    def _compute_payment_term_id_domain(self):
        for record in self:
            cash_days = 0
            current_payment_term_ids = record.current_customer_credit_id.customer_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_payment_term_ids:
                record.domain_payment_term_id = json.dumps(
                ['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.domain_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    domain_vendor_currency_id = fields.Char(
       compute="_compute_vendor_currency_id_domain",
       compute_sudo=True,
       readonly=True,
       store=False,
    )

    @api.onchange('current_vrm_id.vendor_currency_ids')
    @api.depends('current_vrm_id.vendor_currency_ids')
    def _compute_vendor_currency_id_domain(self):
        for record in self:
            current_vendor_currency_ids = record.current_vrm_id.vendor_currency_ids.ids
            if current_vendor_currency_ids:
                record.domain_vendor_currency_id = json.dumps(
                [('id','in',current_vendor_currency_ids)]
                )
            else:
                record.domain_vendor_currency_id = []
                
    domain_vendor_payment_term_id = fields.Char(
       compute="_compute_vendor_payment_term_id_domain",
       compute_sudo=True,
       readonly=True,
       store=False,
    )

    @api.onchange('current_vendor_credit_id.vendor_payment_term_ids')
    @api.depends('current_vendor_credit_id.vendor_payment_term_ids')
    def _compute_vendor_payment_term_id_domain(self):
        for record in self:
            cash_days = 0
            current_payment_term_ids = record.current_vendor_credit_id.vendor_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_payment_term_ids:
                record.domain_vendor_payment_term_id = json.dumps(
                ['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.domain_vendor_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

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

    #purchase teams inherits

    purchase_partner_team_id = fields.Many2one('purchase.team', string="Purchase Team")



class ResUser(models.Model):
    _inherit = 'res.users'

    #application inherits
    
    purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")
