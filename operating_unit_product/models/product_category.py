# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api, _


class ProductCategory(models.Model):
    _inherit = "product.category"

    sales_user_id = fields.Many2one('res.users', string="Sales User")
    sales_ou_id = fields.Many2one('operating.unit', string="Sales Unit", related='sales_user_id.default_operating_unit_sales_id', depends=['sales_user_id.default_operating_unit_sales_id'], store=True, index=True)

    sales_ops_user_id = fields.Many2one('res.users', string="Sales Ops User")
    sales_ops_ou_id = fields.Many2one('operating.unit', string="Sales Ops Unit", related='sales_ops_user_id.default_operating_unit_sales_ops_id', depends=['sales_ops_user_id.default_operating_unit_sales_ops_id'], store=True, index=True)

    procurement_user_id = fields.Many2one('res.users', string="Procurement User")
    procurement_ou_id = fields.Many2one('operating.unit', string="Procurement Unit", related='procurement_user_id.default_operating_unit_procurement_id', depends=['procurement_user_id.default_operating_unit_procurement_id'], store=True, index=True)
    
    procurement_ops_user_id = fields.Many2one('res.users', string="Procurement Ops User")
    procurement_ops_ou_id = fields.Many2one('operating.unit', string="Procurement Ops Unit", related='procurement_ops_user_id.default_operating_unit_procurement_ops_id', depends=['procurement_ops_user_id.default_operating_unit_procurement_ops_id'], store=True, index=True)

    finance_user_id = fields.Many2one('res.users', string="Finance User")
    finance_ou_id = fields.Many2one('operating.unit', string="Finance Unit", related='finance_user_id.default_operating_unit_finance_id', depends=['finance_user_id.default_operating_unit_finance_id'], store=True, index=True)

    finance_ops_user_id = fields.Many2one('res.users', string="Finance Ops User")
    finance_ops_ou_id = fields.Many2one('operating.unit', string="Finance Ops Unit", related='finance_ops_user_id.default_operating_unit_finance_ops_id', depends=['finance_ops_user_id.default_operating_unit_finance_ops_id'], store=True, index=True)

    hr_user_id = fields.Many2one('res.users', string="HR User")
    hr_ou_id = fields.Many2one('operating.unit', string="HR Unit", related='hr_user_id.default_operating_unit_hr_id', depends=['hr_user_id.default_operating_unit_hr_id'], store=True, index=True)

    it_user_id = fields.Many2one('res.users', string="IT User")
    it_ou_id = fields.Many2one('operating.unit', string="IT Unit", related='it_user_id.default_operating_unit_it_id', depends=['it_user_id.default_operating_unit_it_id'], store=True, index=True)

    executive_user_id = fields.Many2one('res.users', string="Executive User")
    executive_ou_id = fields.Many2one('operating.unit', string="Executive Unit", related='executive_user_id.default_operating_unit_executive_id', depends=['executive_user_id.default_operating_unit_executive_id'], store=True, index=True)
