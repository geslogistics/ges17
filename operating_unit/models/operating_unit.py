# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _


class OperatingUnit(models.Model):

    _name = "operating.unit"
    _description = "Operating Unit"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_names_search = ["name", "code"]
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index='trigram', required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for unit in self:
            if unit.parent_id:
                unit.complete_name = '%s / %s' % (unit.parent_id.complete_name, unit.name)
            else:
                unit.complete_name = unit.name

    code = fields.Char(required=True, copy=False)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    parent_id = fields.Many2one('operating.unit',string="Parent Unit", index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many('operating.unit','parent_id', string="Child OU(s)", readonly=True)
    function_selections = [
        ('sales','Sales'),
        ('sales_ops','Sales Operations'),
        ('procurement','Procurement'),
        ('procurement_ops','Procurement Operations'),
        ('finance','Finance'),
        ('finance_ops','Finance Operations'),
        ('hr','HR'),
        ('it','IT'),
        ('marketing','Marketing'),
        ('executive','Executive'),
        ('virtual','Virtual')]
    function = fields.Selection(selection=function_selections, string="Function", default="sales", required=True)
    manager_id = fields.Many2one('res.users', string='Manager', tracking=True, required=True)
    #partner_id = fields.Many2one("res.partner", "Partner", required=True)
    user_ids = fields.Many2many(
        "res.users",
        "operating_unit_users_rel",
        "operating_unit_id",
        "user_id",

        "Users Allowed",
    )
    parent_user_ids = fields.Many2many(
        "res.users",
        "operating_unit_users_of_parent_rel",
        store=True,
        compute="_compute_parent_users",
        compute_sudo=True,
        string="Parent Users Allowed",
    )
    
    @api.depends('parent_id.user_ids','parent_id.parent_user_ids')
    def _compute_parent_users(self):
        for record in self:
            record.parent_user_ids = False
            if record.parent_id:
                record.parent_user_ids = record.parent_id.user_ids + record.parent_id.parent_user_ids

    _sql_constraints = [
        (
            "code_company_uniq",
            "unique (code,company_id)",
            "The code of the operating unit must " "be unique per company!",
        ),
        (
            "name_company_uniq",
            "unique (name,company_id)",
            "The name of the operating unit must " "be unique per company!",
        ),
    ]

    
    def name_get(self):
        res = []
        for ou in self:
            name = ou.name
            if ou.code:
                name = "[{}] {}".format(ou.code, name)
            res.append((ou.id, name))
        return res
    

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.write({"user_ids": [fields.Command.link(self.env.user.id)]})
        self.clear_caches()
        return res

    def write(self, vals):
        self.clear_caches()
        return super().write(vals)


    @api.constrains('parent_id')
    def _check_ou_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive units.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_except_default_operating_unit(self):
        main_operating_unit = self.env.ref('operating_unit.operating_unit_all', raise_if_not_found=False)
        if main_operating_unit and main_operating_unit in self:
            raise UserError(_("You cannot delete this operating unit, it is the default generic operating unit."))
        expense_category = self.env.ref('product.cat_expense', raise_if_not_found=False)
        if expense_category and expense_category in self:
            raise UserError(_("You cannot delete the %s product category.", expense_category.name))