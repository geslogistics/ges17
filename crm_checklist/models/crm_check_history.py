#coding: utf-8

from odoo import fields, models


class crm_check_history(models.Model):
    """
    The model to keep approval history
    """
    _name = "crm.check.history"
    _description = "Checklist History"

    check_list_id = fields.Many2one("crm.check.list", string="Checkpoint")
    lead_id = fields.Many2one("crm.lead", string="Opportunity")
    complete_date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())
    user_id = fields.Many2one("res.users", "User", default=lambda self: self.env.user.id)
    done_action = fields.Selection([("done", "Complete"), ("reset", "Reset")], string="Action", default="done")

    _order = "complete_date DESC,id"
