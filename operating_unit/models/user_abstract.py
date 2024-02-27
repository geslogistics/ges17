from odoo import api, fields, models, _



class UserAbstract(models.AbstractModel):

    _name = 'user.abstract.mixin'
    _description = 'User Abstract Mixin'

    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids")
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True)

    current_operating_unit_sales_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_id", string="Sales Unit")
    current_operating_unit_sales_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_ops_id", string="Sales Ops Unit")
    current_operating_unit_procurement_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_id", string="Procurement Unit")
    current_operating_unit_procurement_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_ops_id", string="Procurement Ops Unit")
    current_operating_unit_finance_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_id", string="Finance Unit")
    current_operating_unit_finance_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_ops_id", string="Finance Ops Unit")
    current_operating_unit_hr_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_hr_id", string="HR Unit")
    current_operating_unit_it_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_it_id", string="IT Unit")
    current_operating_unit_marketing_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_marketing_id", string="Marketing Unit")
    current_operating_unit_executive_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_executive_id", string="Executive Unit")

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
            
    