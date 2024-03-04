# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class CostingRequestUserActionWizard(models.TransientModel):
    _name = 'request.costing.user.action.wizard'

    name = fields.Char(string="Action")
    request_ids = fields.Many2many('request.costing', 'request_user_action_wizard', 'user_action_request' ,'request_user_action_wizard_id', string="Request(s)")
    request_item_ids = fields.Many2many('request.costing.item', 'request_item_action_wizard', 'user_action_item' ,'request_item_action_wizard_id', string="Request Item(s)")
    note = fields.Text(string="Notes")

    def confirm_action(self):
        if self.name == 'req_cost_submit':
            self.request_ids._action_submit(note=self.note)
        elif self.name == 'req_cost_validate':
            self.request_ids._action_validate(note=self.note)
        elif self.name == 'req_cost_return':
            self.request_ids._action_return(note=self.note)
        
        elif self.name == 'req_cost_item_submit_quote':
            self.request_item_ids._submit_quote(note=self.note)
        elif self.name == 'req_cost_item_validate_quote':
            self.request_item_ids._validate_quote(note=self.note)
        elif self.name == 'req_cost_item_return_quote':
            self.request_item_ids._return_quote(note=self.note)
        elif self.name == 'req_cost_item_submit_failed':
            self.request_item_ids._submit_failed(note=self.note)
        elif self.name == 'req_cost_item_validate_failed':
            self.request_item_ids._validate_failed(note=self.note)
        elif self.name == 'req_cost_item_return_failed':
            self.request_item_ids._return_failed(note=self.note)
        elif self.name == 'req_cost_item_recost':
            self.request_item_ids._recost(note=self.note)



        elif self.name == 'req_cost_submit_selection':
            self.request_ids._action_submit_selection(note=self.note)
        elif self.name == 'req_cost_item_confirm_quote':
            self.request_item_ids._confirm_quote(note=self.note)
        elif self.name == 'req_cost_item_reject_quote':
            self.request_item_ids._reject_quote(note=self.note)
        elif self.name == 'req_cost_item_bill_quote':
            self.request_item_ids._bill_quote(note=self.note)
        elif self.name == 'req_cost_item_reject_bill':
            self.request_item_ids._reject_bill(note=self.note)

        elif self.name == 'req_cost_item_cancel':
            self.request_item_ids._cancel_item(note=self.note)
            

        elif self.name == 'req_cost_cancel':
            self.request_ids._action_cancel(note=self.note)


