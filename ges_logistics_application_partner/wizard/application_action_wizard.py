# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class ApplicationActionWizard(models.TransientModel):
    _name = 'application.action.wizard'

    name = fields.Char(string="Action")
    application_ids = fields.Many2many('application.partner', 'app_partner_action_wizard', 'action_application' ,'application_action_wizard_id', string="Application(s)")
    note = fields.Text(string="Notes")

    def confirm_action(self):
        if self.name == 'app_partner_submit':
            self.application_ids._action_submit(note=self.note)

        elif self.name == 'app_partner_validate_unit':
            self.application_ids._action_validate_unit(note=self.note)
        elif self.name == 'app_partner_return_unit':
            self.application_ids._action_return_unit(note=self.note)

        elif self.name == 'app_partner_validate_function':
            self.application_ids._action_validate_function(note=self.note)
        elif self.name == 'app_partner_return_function':
            self.application_ids._action_return_function(note=self.note)
        
        elif self.name == 'app_partner_approve':
            self.application_ids._action_approve(note=self.note)
        elif self.name == 'app_partner_reject':
            self.application_ids._action_reject(note=self.note)

        elif self.name == 'app_partner_cancel':
            self.application_ids._action_cancel(note=self.note)


