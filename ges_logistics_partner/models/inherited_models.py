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
        string="Assigned Salesperson",
        related="pa_partner_id.user_id",
        store=True
        )

    pa_team_id = fields.Many2one(
        'crm.team',
        string="Assigned Sales Team",
        related="pa_user_id.sale_team_id",
        store=True
        )
    
    #purchase teams inherits

    buyer_id = fields.Many2one(
        comodel_name='res.users',
        string="Buyer",
        compute='_compute_buyer_id',
        store=True, index=True,
        )
    
    purchase_team_id = fields.Many2one(
        comodel_name='purchase.team',
        string="Purchase Team",
        compute='_compute_purchase_team_id',
        store=True, index=True,
        )
    
    pa_buyer_id = fields.Many2one(
        'res.users', 
        string="Assigned Buyer", 
        related="pa_partner_id.buyer_id",
        store=True
        )
    
    pa_purchase_team_id = fields.Many2one(
        'purchase.team',
        string="Assigned Purchase Team",
        related="pa_buyer_id.purchase_team_id",
        store=True
        )

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _update_pa_pricelist_id(self):
        for record in self:
            if record.pa_partner_id:
                record.pa_pricelist_id = record.pa_partner_id.property_product_pricelist

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _update_pa_payment_term_id(self):
        for record in self:
            if record.pa_partner_id:
                record.pa_payment_term_id = record.pa_partner_id.property_payment_term_id

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _compute_buyer_id(self):
        for record in self:
            if record.pa_partner_id and not (record._origin.id and record.buyer_id):
                record.buyer_id = record.pa_partner_id.buyer_id

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _compute_purchase_team_id(self):
        for record in self:
            if record.pa_partner_id and not (record._origin.id and record.purchase_team_id):
                record.purchase_team_id = record.pa_partner_id.purchase_partner_team_id

    @api.onchange('pa_partner_id')
    @api.depends('pa_partner_id')
    def _compute_pa_pricelist_id_domain(self):
        for record in self.sudo():
            current_pa_pricelist_ids = record.pa_partner_id.current_crm_id.customer_pricelist_ids.ids
            if current_pa_pricelist_ids:
                record.pa_domain_pricelist_id = json.dumps(
                [('id','in',current_pa_pricelist_ids), ('company_id', 'in', (False, self.env.company.id))]
                )
            else:
                record.pa_domain_pricelist_id = json.dumps(
                [('company_id', 'in', (False, self.env.company.id))]
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
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, self.env.company.id))]
                )

    # update pa fields
    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def update_partner_id_to_pa_field(self):
        if self.is_pa_user:
            self.partner_id = self.pa_partner_id.id

    @api.depends('pa_pricelist_id')
    @api.onchange('pa_pricelist_id')
    def update_pricelist_id_to_pa_field(self):
        if self.is_pa_user:
            self.pricelist_id = self.pa_pricelist_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_payment_term_id_to_pa_field(self):
        if self.is_pa_user:
            self.payment_term_id = self.pa_payment_term_id.id

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

    # reverse update pa fields

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def update_pa_partner_id_to_field(self):
        if not self.is_pa_user:
            self.pa_partner_id = self.partner_id.id

    @api.depends('pricelist_id')
    @api.onchange('pricelist_id')
    def update_pa_pricelist_id_to_field(self):
        if not self.is_pa_user:
            self.pa_pricelist_id = self.pricelist_id.id

    @api.depends('payment_term_id')
    @api.onchange('payment_term_id')
    def update_pa_payment_term_id_to_field(self):
        if not self.is_pa_user:
            self.pa_payment_term_id = self.payment_term_id.id

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


    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        hide_list = [
            'pa_partner_id',
            'pa_pricelist_id',
            'pa_domain_pricelist_id',
            'pa_payment_term_id',
            'pa_domain_payment_term_id',
            #'pa_user_id',
            #'pa_team_id',
            #'buyer_id',
            #'purchase_team_id',
            #'pa_buyer_id',
            #'pa_purchase_team_id',
        ]
        for field in hide_list:
            if res.get(field):
                res[field]['searchable'] = False
                res[field]['selectable'] = False # to hide in Add Custom filter view
                res[field]['sortable'] = False # to hide in group by view
                res[field]['exportable'] = False # to hide in export list
                res[field]['store'] = False # to hide in 'Select Columns' filter in tree views

        return res


    
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
        related="pa_partner_id.buyer_id",
        store=True,
        )
    
    team_id = fields.Many2one(
        comodel_name='purchase.team',
        string="Purchase Team",
        compute='_compute_purchase_team_id',
        store=True, index=True,
        )
    
    pa_team_id = fields.Many2one(
        'purchase.team', 
        string="Assigned Purchase Team", 
        related="pa_user_id.purchase_team_id",
        store=True,
        )

    #sales teams inherits

    sale_user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_sale_user_id',
        store=True, index=True,
        )

    sale_team_id = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
        compute='_compute_sale_team_id',
        store=True, index=True,
        )

    pa_sale_user_id = fields.Many2one(
        'res.users', 
        string="Assigned Salesperson", 
        related="pa_partner_id.user_id",
        store=True,
        )
    
    pa_sale_team_id = fields.Many2one(
        'crm.team',
        string="Assigned Sales Team",
        related="pa_sale_user_id.sale_team_id",
        store=True,
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
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, self.env.company.id))]
                )
    
    
    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _update_pa_currency_id(self):
        for record in self:
            if record.pa_partner_id:
                record.pa_currency_id = record.pa_partner_id.property_purchase_currency_id

    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _update_pa_payment_term_id(self):
        for record in self:
            if record.pa_partner_id:
                record.pa_payment_term_id = record.pa_partner_id.property_supplier_payment_term_id


    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _compute_sale_user_id(self):
        for record in self:
            if record.pa_partner_id and not (record._origin.id and record.sale_user_id):
                record.sale_user_id = record.pa_partner_id.user_id
    
    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _compute_purchase_team_id(self):
        for record in self:
            if record.pa_partner_id and not (record._origin.id and record.team_id):
                record.team_id = record.pa_partner_id.purchase_partner_team_id
    
    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def _compute_sale_team_id(self):
        for record in self:
            if record.pa_partner_id and not (record._origin.id and record.sale_team_id):
                record.sale_team_id = record.pa_partner_id.team_id

    #update pa fields
    @api.depends('pa_partner_id')
    @api.onchange('pa_partner_id')
    def update_partner_id_to_pa_field(self):
        if self.is_pa_user:
            self.partner_id = self.pa_partner_id.id

    @api.depends('pa_currency_id')
    @api.onchange('pa_currency_id')
    def update_currency_id_to_pa_field(self):
        if self.is_pa_user:
            self.currency_id = self.pa_currency_id.id

    @api.depends('pa_payment_term_id')
    @api.onchange('pa_payment_term_id')
    def update_payment_term_id_to_pa_field(self):
        if self.is_pa_user:
            self.payment_term_id = self.pa_payment_term_id.id

    #reverse update pa fields
    @api.depends('partner_id')
    @api.onchange('partner_id')
    def update_pa_partner_id_to_field(self):
        if not self.is_pa_user:
            self.pa_partner_id = self.partner_id.id

    @api.depends('currency_id')
    @api.onchange('currency_id')
    def update_pa_currency_id_to_field(self):
        if not self.is_pa_user:
            self.pa_currency_id = self.currency_id.id

    @api.depends('payment_term_id')
    @api.onchange('payment_term_id')
    def update_pa_payment_term_id_to_field(self):
        if not self.is_pa_user:
            self.pa_payment_term_id = self.payment_term_id.id


    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        hide_list = [
            'current_user_id',
            'is_pa_user',
            'pa_partner_id',
            'pa_currency_id',
            'pa_domain_currency_id',
            'pa_payment_term_id',
            'pa_domain_payment_term_id',
            #'pa_user_id',
            #'team_id',
            #'pa_team_id',
            #'sale_user_id',
            #'sale_team_id',
            #'pa_sale_user_id',
            #'pa_sale_team_id',
        ]
        for field in hide_list:
            if res.get(field):
                res[field]['searchable'] = False
                res[field]['selectable'] = False # to hide in Add Custom filter view
                res[field]['sortable'] = False # to hide in group by view
                res[field]['exportable'] = False # to hide in export list
                res[field]['store'] = False # to hide in 'Select Columns' filter in tree views

        return res







