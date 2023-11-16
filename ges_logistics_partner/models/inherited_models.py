# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #applications inherits

    partner_id = fields.Many2one(
        domain = [('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_crm_state', '=', 'active'),('current_crm_expiry_date', '>', fields.Date.today())]
    )

    domain_pricelist_id = fields.Char(
       compute="_compute_pricelist_id_domain",
       readonly=True,
       store=False,
    )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_pricelist_id_domain(self):
        for record in self:
            record.pricelist_id = False
            current_pricelist_ids = record.partner_id.current_crm_id.customer_pricelist_ids.ids
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
       readonly=True,
       store=False,
    )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_payment_term_id_domain(self):
        for record in self:
            record.payment_term_id = False
            cash_days = 0
            current_payment_term_ids = record.partner_id.current_customer_credit_id.customer_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_payment_term_ids:
                record.domain_payment_term_id = json.dumps(
                ['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.domain_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(
        domain = [('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_vrm_state', '=', 'active'),('current_vrm_expiry_date', '>', fields.Date.today())]
    )
    

    domain_currency_id = fields.Char(
       compute="_compute_currency_id_domain",
       readonly=True,
       store=False,
    )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_currency_id_domain(self):
        for record in self:
            record.currency_id = False
            current_currency_ids = record.partner_id.current_vrm_id.vendor_currency_ids.ids
            if current_currency_ids:
                record.domain_currency_id = json.dumps(
                [('id','in',current_currency_ids)]
                )
            else:
                record.domain_currency_id = []
                
    domain_payment_term_id = fields.Char(
       compute="_compute_payment_term_id_domain",
       readonly=True,
       store=False,
    )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_payment_term_id_domain(self):
        for record in self:
            record.payment_term_id = False
            cash_days = 0
            current_payment_term_ids = record.partner_id.current_vendor_credit_id.vendor_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            if current_payment_term_ids:
                record.domain_payment_term_id = json.dumps(
                ['|',('id','in',current_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
                )
            else:
                record.domain_payment_term_id = json.dumps(
                [('id','not in',non_cash_payment_term_line_ids), ('company_id', 'in', (False, record.company_id.id))]
                )

    #purchase teams inherits

	 
	 
    purchase_team_id = fields.Many2one('purchase.team', string="Purchase Team")



