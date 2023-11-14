# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

READONLY_FIELD_STATES = {state: [('readonly', True)] for state in {'sale', 'done', 'cancel'}}

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    """
    @api.onchange('validity_date','current_kyc_id.state','current_kyc_expiry_date','current_crm_id.state','current_crm_expiry_date')
    def _sale_partner_domain(self):
        saleable_partner_ids = self.env['res.partner'].search([('company_id','=',self.company_id.id)]).filtered(lambda r: r.current_kyc_id.state == 'active' and r.current_kyc_expiry_date > fields.Date.today() and r.current_crm_id.state == 'active' and r.current_crm_expiry_date > fields.Date.today()).ids
        #return [('id', 'in', saleable_partner_ids)]
        raise UserError(saleable_partner_ids)
        return {'domain':{'partner_id':[('id', 'in', saleable_partner_ids)]}}
    """
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False, change_default=True, index=True,
        tracking=1,
        states=READONLY_FIELD_STATES,
        domain=[('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_crm_state', '=', 'active'),('current_crm_expiry_date', '>', fields.Date.today())]
        )
    
    



    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_pricelist_id_domain(self):
        current_pricelist_ids = self.partner_id.current_crm_id.customer_pricelist_ids.ids
        if current_pricelist_ids:
            return {'domain':{'pricelist_id':[('id','in',current_pricelist_ids), ('company_id', 'in', (False, self.company_id.id))]}}
        else:
            return {'domain':{'pricelist_id':"[('company_id', 'in', (False, company_id))]"}}

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_payment_term_id_domain(self):
        self.payment_term_id = False
        cash_months = 0
        cash_days = 0
        current_payment_term_ids = self.partner_id.current_customer_credit_id.customer_payment_term_ids.ids
        non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('months','>',cash_months),('days','>',cash_days)]).payment_id.ids
        if current_payment_term_ids:
            return {'domain':{'payment_term_id':['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]}}
        else:
            return {'domain':{'payment_term_id':[('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, self.company_id.id))]}}

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    """
    def _purchase_partner_domain(self):
        purchaseable_partner_ids = self.env['res.partner'].search([('company_id','=',self.company_id.id)]).filtered(lambda r: r.current_kyc_id.state == 'active' and r.current_kyc_expiry_date > fields.Date.today() and r.current_vrm_id.state == 'active' and r.current_vrm_expiry_date > fields.Date.today()).ids
        return [('id', 'in', purchaseable_partner_ids)] 
    """
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="[('current_kyc_state', '=', 'active'),('current_vrm_state', '=', 'active')]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    
    
    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_currency_id_domain(self):
        self.currency_id = False
        current_currency_ids = self.partner_id.current_vrm_id.vendor_currency_ids.ids
        if current_currency_ids:
            return {'domain':{'currency_id':[('id','in',current_currency_ids)]}}
        else:
            return {'domain':{'currency_id':False}}


    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _update_payment_term_id_domain(self):
        self.payment_term_id = False
        cash_months = 0
        cash_days = 0
        current_payment_term_ids = self.partner_id.current_vendor_credit_id.vendor_payment_term_ids.ids
        non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('months','>',cash_months),('days','>',cash_days)]).payment_id.ids
        
        if current_payment_term_ids:
            return {'domain':{'payment_term_id':['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]}}
        else:
            return {'domain':{'payment_term_id':[('id','not in',non_cash_payment_term_line_ids),('company_id', 'in', (False, self.company_id.id))]}}





