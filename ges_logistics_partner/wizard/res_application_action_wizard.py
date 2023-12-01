# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class ResPartnerApplicationUserActionWizard(models.TransientModel):
    _name = 'res.partner.application.user.action.wizard'

    name = fields.Selection([('submitted','Submitted'),('validated','Validated'),('returned','Returned'),('approved','Approved'),('rejected','Rejected'),('cancelled','Cancelled')], string="Action", no_sort=True)
    application_ids = fields.Many2many('res.partner.application', 'res_pa_user_action_wizard', 'pa_user_action_app' ,'pa_user_action_wizard_id', string="Application(s)")
    note = fields.Text(string="Notes")

    def confirm_action(self):
        if self.name == 'submitted':
            self.application_ids._action_submit(note=self.note)
        elif self.name == 'validated':
            self.application_ids._action_validate(note=self.note)
        elif self.name == 'returned':
            self.application_ids._action_draft(note=self.note)
        elif self.name == 'approved':
            self.application_ids._action_approve(note=self.note)
        elif self.name == 'rejected':
            self.application_ids._action_reject(note=self.note)
        elif self.name == 'cancelled':
            self.application_ids._action_cancel(note=self.note)


