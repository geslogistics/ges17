# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids", store=False)
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True, store=False)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True, store=False)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True, store=False)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True, store=False)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True, store=False)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True, store=False)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True, store=False)

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

    @api.depends("current_user_id", "current_operating_unit_ids")
    def _compute_current_operating_unit_ids(self):
        for user in self:
            user.current_operating_unit_sales_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales')
            user.current_operating_unit_sales_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')
            user.current_operating_unit_procurement_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement')
            user.current_operating_unit_procurement_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')
            user.current_operating_unit_finance_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance')
            user.current_operating_unit_finance_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')
            user.current_operating_unit_hr_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'hr')
            user.current_operating_unit_it_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'it')
            user.current_operating_unit_executive_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'executive')
            user.current_operating_unit_virtual_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'virtual')
            
    
    
    partner_id = fields.Many2one(
        domain = [('current_kyc_state', '=', 'active'),('current_kyc_expiry_date', '>', fields.Date.today()),('current_crm_state', '=', 'active'),('current_crm_expiry_date', '>', fields.Date.today())],
    )

    pa_domain_pricelist_id = fields.Char(
        compute="_compute_pa_pricelist_id_domain",
        readonly=True,
        store=False,
        )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_pa_pricelist_id_domain(self):
        for record in self.sudo():
            current_pa_pricelist_ids = record.partner_id.current_crm_id.customer_pricelist_ids.ids
            record.pa_domain_pricelist_id = json.dumps(
            [('id','in',current_pa_pricelist_ids), ('company_id', 'in', (False, self.env.company.id))]
            )

                
    pa_domain_payment_term_id = fields.Char(
       compute="_compute_pa_payment_term_id_domain",
       readonly=True,
       store=False,
       )

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _compute_pa_payment_term_id_domain(self):
        for record in self.sudo():
            cash_days = 0
            current_pa_payment_term_ids = record.partner_id.current_customer_credit_id.customer_payment_term_ids.ids
            non_cash_payment_term_line_ids = self.env['account.payment.term.line'].search(['|',('nb_days','>',cash_days),('delay_type','!=','days_after')]).payment_id.ids
            
            record.pa_domain_payment_term_id = json.dumps(
            ['|',('id','in',current_pa_payment_term_ids),('id','not in',non_cash_payment_term_line_ids)]
            )
