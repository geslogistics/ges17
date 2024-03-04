#coding: utf-8

from odoo import fields, models


class crm_stage(models.Model):
    """
    Overwrite to add checklist and checklist settings
    """
    _inherit = "crm.stage"

    default_crm_check_list_ids = fields.One2many("crm.check.list", "crm_stage_st_id", string="Checklist")
    no_need_for_checklist = fields.Boolean(
        string="No need for checklist",
        help="If checked, when you move a case TO this stage, no checklist is required (e.g. for 'Cancelled')"
    )
    cannot_be_missed = fields.Boolean(
        string="Forbid skipping this stage",
        help="If checked, this stage cannot be skipped if a case is moved further. The setting does not influence \
'No need for checklist' progress."
    )
    forbid_back_progress = fields.Boolean(
        string="Forbid regression to this stage",
        help="If checked, moving a case back TO this stage from further stages will be impossible",
    )

    requires_kyc = fields.Boolean(string="KYC")
    requires_crm = fields.Boolean(string="CRM")
    requires_cc = fields.Boolean(string="CC")
    requires_cs = fields.Boolean(string="CS")
    requires_vrm = fields.Boolean(string="VRM")
    requires_vc = fields.Boolean(string="VC")
    requires_vs = fields.Boolean(string="VS")