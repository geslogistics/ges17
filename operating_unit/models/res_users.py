# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def default_get(self, fields):
        vals = super(ResUsers, self).default_get(fields)
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_setup.default_user_rights", "False")
            == "True"
        ):
            default_user = self.env.ref("base.default_user")
            vals[
                "default_operating_unit_id"
            ] = default_user.default_operating_unit_id.id
            vals["operating_unit_ids"] = [(6, 0, default_user.operating_unit_ids.ids)]
        return vals


    @api.model
    def operating_unit_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_id

    @api.model
    def _default_operating_unit(self):
        return self.operating_unit_default_get()

    @api.model
    def _default_operating_units(self):
        return self._default_operating_unit()

    operating_unit_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_ids",
        inverse="_inverse_operating_unit_ids",
        string="Allowed Units",
        compute_sudo=True,
    )

    assigned_operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_users_rel",
        column1="user_id",
        column2="operating_unit_id",
        string="Allowed Units",
        default=lambda self: self._default_operating_units(),
    )

    default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Unit",
        default=lambda self: self._default_operating_unit(),
        domain="[('company_id', '=', current_company_id)]",
    )

    @api.onchange("operating_unit_ids")
    def _onchange_operating_unit_ids(self):
        for record in self:
            if (
                record.default_operating_unit_id
                and record.default_operating_unit_id
                not in record.operating_unit_ids._origin
            ):
                record.default_operating_unit_id = False

    @api.depends("groups_id", "assigned_operating_unit_ids")
    def _compute_operating_unit_ids(self):
        for user in self:
            if user._origin.has_group("operating_unit.group_manager_operating_unit"):
                dom = []
                if self.env.context.get("allowed_company_ids"):
                    dom = [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "in", self.env.context["allowed_company_ids"]),
                    ]
                else:
                    dom = []
                user.operating_unit_ids = self.env["operating.unit"].sudo().search(dom)
            else:
                user.operating_unit_ids = user.assigned_operating_unit_ids


    def _inverse_operating_unit_ids(self):
        for user in self:
            user.assigned_operating_unit_ids = user.operating_unit_ids
        self.clear_caches()



    ######### Sales OUs  #########

    @api.model
    def operating_unit_sales_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_sales_id

    @api.model
    def _default_operating_unit_sales(self):
        return self.operating_unit_sales_default_get()

    @api.model
    def _default_operating_unit_saless_sales(self):
        return self._default_operating_unit_sales()

    operating_unit_sales_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_sales_ids",
        string="Sales Units",
        compute_sudo=True,
    )

    assigned_operating_unit_sales_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_sales_users_rel",
        column1="user_id",
        column2="operating_unit_sales_id",
        string="Sales Units",
        default=lambda self: self._default_operating_unit_saless_sales(),
    )

    default_operating_unit_sales_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Sales Unit",
        default=lambda self: self._default_operating_unit_sales(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_sales_ids.ids)]",
    )
    
    @api.onchange("operating_unit_sales_ids")
    def _onchange_operating_unit_sales_ids(self):
        for record in self:
            if (
                record.default_operating_unit_sales_id
                and record.default_operating_unit_sales_id
                not in record.operating_unit_sales_ids._origin
            ):
                record.default_operating_unit_sales_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_sales_ids(self):
        for user in self:
            user.operating_unit_sales_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'sales')


    ######### Sales Ops OUs  #########

    @api.model
    def operating_unit_sales_ops_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_sales_ops_id

    @api.model
    def _default_operating_unit_sales_ops(self):
        return self.operating_unit_sales_ops_default_get()

    @api.model
    def _default_operating_unit_sales_opss_sales_ops(self):
        return self._default_operating_unit_sales_ops()

    operating_unit_sales_ops_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_sales_ops_ids",
        string="Sales Ops Units",
        compute_sudo=True,
    )

    assigned_operating_unit_sales_ops_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_sales_ops_users_rel",
        column1="user_id",
        column2="operating_unit_sales_ops_id",
        string="Sales Ops Units",
        default=lambda self: self._default_operating_unit_sales_opss_sales_ops(),
    )

    default_operating_unit_sales_ops_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Sales Ops Unit",
        default=lambda self: self._default_operating_unit_sales_ops(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_sales_ops_ids.ids)]",
    )
    
    @api.onchange("operating_unit_sales_ops_ids")
    def _onchange_operating_unit_sales_ops_ids(self):
        for record in self:
            if (
                record.default_operating_unit_sales_ops_id
                and record.default_operating_unit_sales_ops_id
                not in record.operating_unit_sales_ops_ids._origin
            ):
                record.default_operating_unit_sales_ops_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_sales_ops_ids(self):
        for user in self:
            user.operating_unit_sales_ops_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')

    
    

    ######### Procurement OUs  #########

    @api.model
    def operating_unit_procurement_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_procurement_id

    @api.model
    def _default_operating_unit_procurement(self):
        return self.operating_unit_procurement_default_get()

    @api.model
    def _default_operating_unit_procurements_procurement(self):
        return self._default_operating_unit_procurement()

    operating_unit_procurement_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_procurement_ids",
        string="Procurement Units",
        compute_sudo=True,
    )

    assigned_operating_unit_procurement_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_procurement_users_rel",
        column1="user_id",
        column2="operating_unit_procurement_id",
        string="Procurement Units",
        default=lambda self: self._default_operating_unit_procurements_procurement(),
    )

    default_operating_unit_procurement_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Procurement Unit",
        default=lambda self: self._default_operating_unit_procurement(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_procurement_ids.ids)]",
    )
    
    @api.onchange("operating_unit_procurement_ids")
    def _onchange_operating_unit_procurement_ids(self):
        for record in self:
            if (
                record.default_operating_unit_procurement_id
                and record.default_operating_unit_procurement_id
                not in record.operating_unit_procurement_ids._origin
            ):
                record.default_operating_unit_procurement_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_procurement_ids(self):
        for user in self:
            user.operating_unit_procurement_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'procurement')

######### Procurement Ops OUs  #########

    @api.model
    def operating_unit_procurement_ops_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_procurement_ops_id

    @api.model
    def _default_operating_unit_procurement_ops(self):
        return self.operating_unit_procurement_ops_default_get()

    @api.model
    def _default_operating_unit_procurement_opss_procurement_ops(self):
        return self._default_operating_unit_procurement_ops()

    operating_unit_procurement_ops_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_procurement_ops_ids",
        string="Procurement Ops Units",
        compute_sudo=True,
    )

    assigned_operating_unit_procurement_ops_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_procurement_ops_users_rel",
        column1="user_id",
        column2="operating_unit_procurement_ops_id",
        string="Procurement Ops Units",
        default=lambda self: self._default_operating_unit_procurement_opss_procurement_ops(),
    )

    default_operating_unit_procurement_ops_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Procurement Ops Unit",
        default=lambda self: self._default_operating_unit_procurement_ops(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_procurement_ops_ids.ids)]",
    )
    
    @api.onchange("operating_unit_procurement_ops_ids")
    def _onchange_operating_unit_procurement_ops_ids(self):
        for record in self:
            if (
                record.default_operating_unit_procurement_ops_id
                and record.default_operating_unit_procurement_ops_id
                not in record.operating_unit_procurement_ops_ids._origin
            ):
                record.default_operating_unit_procurement_ops_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_procurement_ops_ids(self):
        for user in self:
            user.operating_unit_procurement_ops_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')


    
######### Finance OUs  #########

    @api.model
    def operating_unit_finance_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_finance_id

    @api.model
    def _default_operating_unit_finance(self):
        return self.operating_unit_finance_default_get()

    @api.model
    def _default_operating_unit_finances_finance(self):
        return self._default_operating_unit_finance()

    operating_unit_finance_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_finance_ids",
        string="Finance Units",
        compute_sudo=True,
    )

    assigned_operating_unit_finance_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_finance_users_rel",
        column1="user_id",
        column2="operating_unit_finance_id",
        string="Finance Units",
        default=lambda self: self._default_operating_unit_finances_finance(),
    )

    default_operating_unit_finance_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Finance Unit",
        default=lambda self: self._default_operating_unit_finance(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_finance_ids.ids)]",
    )
    
    @api.onchange("operating_unit_finance_ids")
    def _onchange_operating_unit_finance_ids(self):
        for record in self:
            if (
                record.default_operating_unit_finance_id
                and record.default_operating_unit_finance_id
                not in record.operating_unit_finance_ids._origin
            ):
                record.default_operating_unit_finance_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_finance_ids(self):
        for user in self:
            user.operating_unit_finance_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'finance')

    ######### Finance Ops OUs  #########

    @api.model
    def operating_unit_finance_ops_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_finance_ops_id

    @api.model
    def _default_operating_unit_finance_ops(self):
        return self.operating_unit_finance_ops_default_get()

    @api.model
    def _default_operating_unit_finance_opss_finance_ops(self):
        return self._default_operating_unit_finance_ops()

    operating_unit_finance_ops_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_finance_ops_ids",
        string="Finance Ops Units",
        compute_sudo=True,
    )

    assigned_operating_unit_finance_ops_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_finance_ops_users_rel",
        column1="user_id",
        column2="operating_unit_finance_ops_id",
        string="Finance Ops Units",
        default=lambda self: self._default_operating_unit_finance_opss_finance_ops(),
    )

    default_operating_unit_finance_ops_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Finance Ops Unit",
        default=lambda self: self._default_operating_unit_finance_ops(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_finance_ops_ids.ids)]",
    )
    
    @api.onchange("operating_unit_finance_ops_ids")
    def _onchange_operating_unit_finance_ops_ids(self):
        for record in self:
            if (
                record.default_operating_unit_finance_ops_id
                and record.default_operating_unit_finance_ops_id
                not in record.operating_unit_finance_ops_ids._origin
            ):
                record.default_operating_unit_finance_ops_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_finance_ops_ids(self):
        for user in self:
            user.operating_unit_finance_ops_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')


    ######### HR OUs  #########

    @api.model
    def operating_unit_hr_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_hr_id

    @api.model
    def _default_operating_unit_hr(self):
        return self.operating_unit_hr_default_get()

    @api.model
    def _default_operating_unit_hrs_hr(self):
        return self._default_operating_unit_hr()

    operating_unit_hr_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_hr_ids",
        string="HR Units",
        compute_sudo=True,
    )

    assigned_operating_unit_hr_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_hr_users_rel",
        column1="user_id",
        column2="operating_unit_hr_id",
        string="HR Units",
        default=lambda self: self._default_operating_unit_hrs_hr(),
    )

    default_operating_unit_hr_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned HR Unit",
        default=lambda self: self._default_operating_unit_hr(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_hr_ids.ids)]",
    )
    
    @api.onchange("operating_unit_hr_ids")
    def _onchange_operating_unit_hr_ids(self):
        for record in self:
            if (
                record.default_operating_unit_hr_id
                and record.default_operating_unit_hr_id
                not in record.operating_unit_hr_ids._origin
            ):
                record.default_operating_unit_hr_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_hr_ids(self):
        for user in self:
            user.operating_unit_hr_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'hr')
    

    
    ######### IT OUs  #########

    @api.model
    def operating_unit_it_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_it_id

    @api.model
    def _default_operating_unit_it(self):
        return self.operating_unit_it_default_get()

    @api.model
    def _default_operating_unit_its_it(self):
        return self._default_operating_unit_it()

    operating_unit_it_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_it_ids",
        string="IT Units",
        compute_sudo=True,
    )

    assigned_operating_unit_it_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_it_users_rel",
        column1="user_id",
        column2="operating_unit_it_id",
        string="IT Units",
        default=lambda self: self._default_operating_unit_its_it(),
    )

    default_operating_unit_it_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned IT Unit",
        default=lambda self: self._default_operating_unit_it(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_it_ids.ids)]",
    )
    
    @api.onchange("operating_unit_it_ids")
    def _onchange_operating_unit_it_ids(self):
        for record in self:
            if (
                record.default_operating_unit_it_id
                and record.default_operating_unit_it_id
                not in record.operating_unit_it_ids._origin
            ):
                record.default_operating_unit_it_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_it_ids(self):
        for user in self:
            user.operating_unit_it_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'it')



    ######### Marketing OUs  #########

    @api.model
    def operating_unit_marketing_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_marketing_id

    @api.model
    def _default_operating_unit_marketing(self):
        return self.operating_unit_marketing_default_get()

    @api.model
    def _default_operating_unit_marketings_marketing(self):
        return self._default_operating_unit_marketing()

    operating_unit_marketing_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_marketing_ids",
        string="Marketing Units",
        compute_sudo=True,
    )

    assigned_operating_unit_marketing_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_marketing_users_rel",
        column1="user_id",
        column2="operating_unit_marketing_id",
        string="Marketing Units",
        default=lambda self: self._default_operating_unit_marketings_marketing(),
    )

    default_operating_unit_marketing_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Marketing Unit",
        default=lambda self: self._default_operating_unit_marketing(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_marketing_ids.ids)]",
    )
    
    @api.onchange("operating_unit_marketing_ids")
    def _onchange_operating_unit_marketing_ids(self):
        for record in self:
            if (
                record.default_operating_unit_marketing_id
                and record.default_operating_unit_marketing_id
                not in record.operating_unit_marketing_ids._origin
            ):
                record.default_operating_unit_marketing_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_marketing_ids(self):
        for user in self:
            user.operating_unit_marketing_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'marketing')

    ######### Executive OUs  #########

    @api.model
    def operating_unit_executive_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_executive_id

    @api.model
    def _default_operating_unit_executive(self):
        return self.operating_unit_executive_default_get()

    @api.model
    def _default_operating_unit_executives_executive(self):
        return self._default_operating_unit_executive()

    operating_unit_executive_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_executive_ids",
        string="Executive Units",
        compute_sudo=True,
    )

    assigned_operating_unit_executive_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_executive_users_rel",
        column1="user_id",
        column2="operating_unit_executive_id",
        string="Executive Units",
        default=lambda self: self._default_operating_unit_executives_executive(),
    )

    default_operating_unit_executive_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Executive Unit",
        default=lambda self: self._default_operating_unit_executive(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_executive_ids.ids)]",
    )
    
    @api.onchange("operating_unit_executive_ids")
    def _onchange_operating_unit_executive_ids(self):
        for record in self:
            if (
                record.default_operating_unit_executive_id
                and record.default_operating_unit_executive_id
                not in record.operating_unit_executive_ids._origin
            ):
                record.default_operating_unit_executive_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_executive_ids(self):
        for user in self:
            user.operating_unit_executive_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'executive')

    ######### Virtual OUs  #########

    @api.model
    def operating_unit_virtual_default_get(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_virtual_id

    @api.model
    def _default_operating_unit_virtual(self):
        return self.operating_unit_virtual_default_get()

    @api.model
    def _default_operating_unit_virtuals_virtual(self):
        return self._default_operating_unit_virtual()

    operating_unit_virtual_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_virtual_ids",
        string="Virtual Units",
        compute_sudo=True,
    )

    assigned_operating_unit_virtual_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_virtual_users_rel",
        column1="user_id",
        column2="operating_unit_virtual_id",
        string="Virtual Units",
        default=lambda self: self._default_operating_unit_virtuals_virtual(),
    )

    default_operating_unit_virtual_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Assigned Virtual Unit",
        default=lambda self: self._default_operating_unit_virtual(),
        domain="[('company_id', '=', current_company_id),('id','in',operating_unit_virtual_ids.ids)]",
    )
    
    @api.onchange("operating_unit_virtual_ids")
    def _onchange_operating_unit_virtual_ids(self):
        for record in self:
            if (
                record.default_operating_unit_virtual_id
                and record.default_operating_unit_virtual_id
                not in record.operating_unit_virtual_ids._origin
            ):
                record.default_operating_unit_virtual_id = False
    
    @api.depends("operating_unit_ids")
    def _compute_operating_unit_virtual_ids(self):
        for user in self:
            user.operating_unit_virtual_ids = user.operating_unit_ids.filtered(lambda r: r.function == 'virtual')