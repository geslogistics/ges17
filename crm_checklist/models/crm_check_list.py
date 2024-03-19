#coding: utf-8

from odoo import _, fields, models
from odoo.exceptions import AccessError
from ..models.crm_lead import SuperRightsCheck


ACESSERRORMESSAGE = _(u"Sorry, but you don't have the right to confirm/disapprove '{0}'! \
Please contact your system administrator for assistance.")


class crm_check_list(models.Model):
    """
    The model to keep check list items
    """
    _name = "crm.check.list"
    _description = "Check List"

    name = fields.Char(string="What should be done on this stage", required=True)
    description = fields.Text(string="Notes")
    crm_stage_st_id = fields.Many2one("crm.stage", string="CRM Stage", required=True)
    team_ids = fields.Many2many(
        "crm.team",
        "crm_team_crm_check_list_rel_table",
        "crm_team_id",
        "crm_check_list_id",
        string="Only for teams",
        help="If not defined, this checkpoint will be applied for opportunities for all teams",
    )
    group_ids = fields.Many2many(
        "res.groups",
        "res_groups_crm_check_list_rel_table",
        "res_groups_id",
        "crm_check_list_id",
        string="User groups",
        help="Only users of those groups will be able to approve this checkpoint. Leave it empty if any user may \
confirm this item",
    )
    should_be_reset = fields.Boolean(
        string="Not saved",
        help="If checked each time an opportunity is reset back to this stage, this checkpoint should be confirmed \
disregarding whether it has been confirmed before",
    )
    sequence = fields.Integer(string="Sequence")

    _order = "sequence, id"

    @SuperRightsCheck
    def action_check_cheklist_rights(self):
        """
        The method to check rights to fill check list item
        """
        for item in self:
            if item.group_ids and not (self.env.user.groups_id & item.group_ids):
                raise AccessError(ACESSERRORMESSAGE.format(item.name))
        return True

    def _get_filtered(self, stage_id, team_id):
        """
        The method to make sure checkpoint relates to the exact stage and team

        Args:
         * stage_id - crm.stage object
         * team_id - crm.team object

        Returns:
         * crm.check.list recordset
        """
        final_checkpoint_ids = self.env["crm.check.list"]
        if self:
            for item in self:
                if item.crm_stage_st_id == stage_id:
                    if not item.sudo().team_ids:
                        final_checkpoint_ids += item
                    elif team_id and team_id.id in item.sudo().team_ids.ids:
                        final_checkpoint_ids += item
        return final_checkpoint_ids
