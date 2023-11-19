# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    is_pa_user = fields.Boolean(string="Is PA User", compute="_compute_is_pa_user", store=False)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs')
    
    
    #applications inherits

    pa_partner_id = fields.Many2one(
        'res.partner', 
        string="Customer",
        domain = [('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_crm_state', '=', 'active'),('current_crm_expiry_date', '>', fields.Date.today())],
        store=True,
        ondelete='restrict',
        )

    pa_pricelist_id = fields.Many2one(
        'product.pricelist',
        string="Pricelist",
        store=True,
        ondelete='restrict',
        )
    
    pa_domain_pricelist_id = fields.Char(
        compute="_compute_pa_pricelist_id_domain",
        readonly=True,
        store=False,
        )

    pa_payment_term_id = fields.Many2one(
        'account.payment.term',
        string="Payment Terms",
        store=True,
        ondelete='restrict',
        )
                
    pa_domain_payment_term_id = fields.Char(
       compute="_compute_pa_payment_term_id_domain",
       readonly=True,
       store=False,
       )

    #sales teams inherits
    pa_user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        related="pa_partner_id.user_id"
        )

    pa_team_id = fields.Many2one(
        'crm.team',
        string="Sales Team",
        related="pa_user_id.sale_team_id"
        )
    
    #purchase teams inherits
    buyer_id = fields.Many2one(
        'res.users', 
        string="Buyer", 
        related="pa_partner_id.buyer_id"
        )
    
    purchase_team_id = fields.Many2one(
        'purchase.team',
        string="Purchase Team",
        related="buyer_id.purchase_team_id"
        )


    @api.onchange('pa_partner_id')
    @api.depends('pa_partner_id')
    def _compute_pa_pricelist_id_domain(self):
        for record in self.sudo():
            current_pa_pricelist_ids = record.pa_partner_id.current_crm_id.customer_pricelist_ids.ids
            if current_pa_pricelist_ids:
                record.pa_domain_pricelist_id = json.dumps(
                [('id','in',current_pa_pricelist_ids), ('company_id', 'in', (False, record.company_id.id))]
                )
            else:
                record.pa_domain_pricelist_id = json.dumps(
                [('company_id', 'in', (False, record.company_id.id))]
                )

    @api.onchange('pa_partner_id')
    @api.depends('pa_partner_id')
    def _compute_pa_payment_term_id_domain(self):
        for record in self.sudo():
            cash_days = 0
            current_pa_payment_term_ids = record.pa_partner_id.current_customer_credit_id.customer_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_pa_payment_term_ids:
                record.pa_domain_payment_term_id = json.dumps(
                ['|',('id','in',current_pa_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.pa_domain_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def update_partner_id_to_pa_field(self):
        self.partner_id = self.pa_partner_id.id

    @api.depends('pa_pricelist_id')
    @api.onchange('pa_pricelist_id')
    def update_pricelist_id_to_pa_field(self):
        self.pricelist_id = self.pa_pricelist_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_payment_term_id_to_pa_field(self):
        self.payment_term_id = self.pa_payment_term_id.id

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

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    is_pa_user = fields.Boolean(string="Is PA User", compute="_compute_is_pa_user", store=False)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs')
    

    #applications inherits
    
    pa_partner_id = fields.Many2one(
        'res.partner', 
        string="Vendor",
        domain = [('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_vrm_state', '=', 'active'),('current_vrm_expiry_date', '>', fields.Date.today())],
        store=True,
        ondelete='restrict',
        )

    pa_currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        store=True,
        ondelete='restrict',
        )
    
    pa_domain_currency_id = fields.Char(
        compute="_compute_pa_currency_id_domain",
        readonly=True,
        store=False,
        )

    pa_payment_term_id = fields.Many2one(
        'account.payment.term',
        string="Payment Terms",
        store=True,
        ondelete='restrict',
        )
                
    pa_domain_payment_term_id = fields.Char(
       compute="_compute_pa_payment_term_id_domain",
       readonly=True,
       store=False,
       )

    #purchase teams inherits
    pa_user_id = fields.Many2one(
        'res.users',
        string="Buyer",
        related="pa_partner_id.buyer_id"
        )

    purchase_team_id = fields.Many2one(
        'purchase.team',
        string="Purchase Team",
        related="pa_user_id.purchase_team_id"
        )

    #sales teams inherits
    sale_user_id = fields.Many2one(
        'res.users', 
        string="Salesperson", 
        related="pa_partner_id.user_id"
        )
    
    sale_team_id = fields.Many2one(
        'crm.team',
        string="Sales Team",
        related="pa_user_id.sale_team_id"
        )
    
    @api.onchange('pa_partner_id')
    @api.depends('pa_partner_id')
    def _compute_pa_currency_id_domain(self):
        for record in self.sudo():
            current_pa_currency_ids = record.pa_partner_id.current_vrm_id.vendor_currency_ids.ids
            if current_pa_currency_ids:
                record.pa_domain_currency_id = json.dumps(
                [('id','in',current_pa_currency_ids)]
                )
            else:
                record.pa_domain_currency_id = []

    @api.onchange('pa_partner_id')
    @api.depends('pa_partner_id')
    def _compute_pa_payment_term_id_domain(self):
        for record in self.sudo():
            cash_days = 0
            current_pa_payment_term_ids = record.pa_partner_id.current_vendor_credit_id.vendor_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_pa_payment_term_ids:
                record.pa_domain_payment_term_id = json.dumps(
                ['|',('id','in',current_pa_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.pa_domain_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def update_partner_id_to_pa_field(self):
        self.partner_id = self.pa_partner_id.id

    @api.depends('pa_currency_id')
    @api.onchange('pa_currency_id')
    def update_currency_id_to_pa_field(self):
        self.currency_id = self.pa_currency_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_payment_term_id_to_pa_field(self):
        self.payment_term_id = self.pa_payment_term_id.id

    @api.depends('pa_user_id')
    @api.onchange('pa_user_id')
    def update_user_id_to_pa_field(self):
        self.user_id = self.pa_user_id.id

    







