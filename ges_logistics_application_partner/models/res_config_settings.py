# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    partner_kyc_submitter_ids = fields.Many2many('res.users', 'submitters_kyc_applications', 'user_id', 'kyc_application_id', string='KYC Submitters')

    partner_kyc_validator_ids = fields.Many2many('res.users', 'validators_kyc_applications', 'user_id', 'kyc_application_id', string='KYC Validators')
    partner_kyc_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_kyc_validator_ids_decision')
    
    partner_kyc_approver_ids = fields.Many2many('res.users', 'approvers_kyc_applications', 'user_id', 'kyc_application_id', string='KYC Approvers')
    partner_kyc_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_kyc_approver_ids_decision')

    partner_crm_submitter_ids = fields.Many2many('res.users', 'submitters_crm_applications', 'user_id', 'crm_application_id', string='CRM Submitters')

    partner_crm_validator_ids = fields.Many2many('res.users', 'validators_crm_applications', 'user_id', 'crm_application_id', string='CRM Validators')
    partner_crm_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_crm_validator_ids_decision')

    partner_crm_approver_ids = fields.Many2many('res.users', 'approvers_crm_applications', 'user_id', 'crm_application_id', string='CRM Approvers')
    partner_crm_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_crm_approver_ids_decision')

    partner_customer_credit_submitter_ids = fields.Many2many('res.users', 'submitters_customer_credit_applications', 'user_id', 'customer_credit_application_id', string='Customer Credit Submitters')

    partner_customer_credit_validator_ids = fields.Many2many('res.users', 'validators_customer_credit_applications', 'user_id', 'customer_credit_application_id', string='Customer Credit Validators')
    partner_customer_credit_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_customer_credit_validator_ids_decision')

    partner_customer_credit_approver_ids = fields.Many2many('res.users', 'approvers_customer_credit_applications', 'user_id', 'customer_credit_application_id', string='Customer Credit Approvers')
    partner_customer_credit_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_customer_credit_approver_ids_decision')

    partner_customer_strategy_submitter_ids = fields.Many2many('res.users', 'submitters_customer_strategy_applications', 'user_id', 'customer_strategy_application_id', string='Customer Strategy Submitters')

    partner_customer_strategy_validator_ids = fields.Many2many('res.users', 'validators_customer_strategy_applications', 'user_id', 'customer_strategy_application_id', string='Customer Strategy Validators')
    partner_customer_strategy_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_customer_strategy_validator_ids_decision')

    partner_customer_strategy_approver_ids = fields.Many2many('res.users', 'approvers_customer_strategy_applications', 'user_id', 'customer_strategy_application_id', string='Customer Strategy Approvers')
    partner_customer_strategy_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_customer_strategy_approver_ids_decision')

    partner_vrm_submitter_ids = fields.Many2many('res.users', 'submitters_vrm_applications', 'user_id', 'vrm_application_id', string='VRM Submitters')

    partner_vrm_validator_ids = fields.Many2many('res.users', 'validators_vrm_applications', 'user_id', 'vrm_application_id', string='VRM Validators')
    partner_vrm_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vrm_validator_ids_decision')

    partner_vrm_approver_ids = fields.Many2many('res.users', 'approvers_vrm_applications', 'user_id', 'vrm_application_id', string='VRM Approvers')
    partner_vrm_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vrm_approver_ids_decision')

    partner_vendor_credit_submitter_ids = fields.Many2many('res.users', 'submitters_vendor_credit_applications', 'user_id', 'vendor_credit_application_id', string='Vendor Credit Submitters')

    partner_vendor_credit_validator_ids = fields.Many2many('res.users', 'validators_vendor_credit_applications', 'user_id', 'vendor_credit_application_id', string='Vendor Credit Validators')
    partner_vendor_credit_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vendor_credit_validator_ids_decision')

    partner_vendor_credit_approver_ids = fields.Many2many('res.users', 'approvers_vendor_credit_applications', 'user_id', 'vendor_credit_application_id', string='Vendor Credit Approvers')
    partner_vendor_credit_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vendor_credit_approver_ids_decision')

    partner_vendor_strategy_submitter_ids = fields.Many2many('res.users', 'submitters_vendor_strategy_applications', 'user_id', 'vendor_strategy_application_id', string='Vendor Strategy Submitters')

    partner_vendor_strategy_validator_ids = fields.Many2many('res.users', 'validators_vendor_strategy_applications', 'user_id', 'vendor_strategy_application_id', string='Vendor Strategy Validators')
    partner_vendor_strategy_validator_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vendor_strategy_validator_ids_decision')

    partner_vendor_strategy_approver_ids = fields.Many2many('res.users', 'approvers_vendor_strategy_applications', 'user_id', 'vendor_strategy_application_id', string='Vendor Strategy Approvers')
    partner_vendor_strategy_approver_ids_decision = fields.Selection([('singly','Singly'),('jointly','Jointly')], string="Decision Making", default="jointly", config_parameter='ges_logistics_application_partner.partner_vendor_strategy_approver_ids_decision')

    def set_values(self):    	
        res = super(ResConfigSettings, self).set_values()    
        	
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_kyc_submitter_ids', self.partner_kyc_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_kyc_validator_ids', self.partner_kyc_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_kyc_approver_ids', self.partner_kyc_approver_ids.ids)
        
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_crm_submitter_ids', self.partner_crm_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_crm_validator_ids', self.partner_crm_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_crm_approver_ids', self.partner_crm_approver_ids.ids)

        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_credit_submitter_ids', self.partner_customer_credit_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_credit_validator_ids', self.partner_customer_credit_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_credit_approver_ids', self.partner_customer_credit_approver_ids.ids)
        
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_strategy_submitter_ids', self.partner_customer_strategy_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_strategy_validator_ids', self.partner_customer_strategy_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_customer_strategy_approver_ids', self.partner_customer_strategy_approver_ids.ids)
        
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vrm_submitter_ids', self.partner_vrm_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vrm_validator_ids', self.partner_vrm_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vrm_approver_ids', self.partner_vrm_approver_ids.ids)

        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_credit_submitter_ids', self.partner_vendor_credit_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_credit_validator_ids', self.partner_vendor_credit_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_credit_approver_ids', self.partner_vendor_credit_approver_ids.ids)
        
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_strategy_submitter_ids', self.partner_vendor_strategy_submitter_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_strategy_validator_ids', self.partner_vendor_strategy_validator_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('ges_logistics_application_partner.partner_vendor_strategy_approver_ids', self.partner_vendor_strategy_approver_ids.ids)


        self.env.ref('ges_logistics_application_partner.group_partner_application_user_submit').users = [(6, 0, self.partner_kyc_submitter_ids.ids + self.partner_crm_submitter_ids.ids + self.partner_customer_credit_submitter_ids.ids + self.partner_customer_strategy_submitter_ids.ids + self.partner_vrm_submitter_ids.ids + self.partner_vendor_credit_submitter_ids.ids + self.partner_vendor_strategy_submitter_ids.ids)]
        self.env.ref('ges_logistics_application_partner.group_partner_application_user_validate').users = [(6, 0, self.partner_kyc_validator_ids.ids + self.partner_crm_validator_ids.ids + self.partner_customer_credit_validator_ids.ids + self.partner_customer_strategy_validator_ids.ids + self.partner_vrm_validator_ids.ids + self.partner_vendor_credit_validator_ids.ids + self.partner_vendor_strategy_validator_ids.ids)]
        self.env.ref('ges_logistics_application_partner.group_partner_application_user_return_draft').users = [(6, 0, self.partner_kyc_validator_ids.ids + self.partner_crm_validator_ids.ids + self.partner_customer_credit_validator_ids.ids + self.partner_customer_strategy_validator_ids.ids + self.partner_vrm_validator_ids.ids + self.partner_vendor_credit_validator_ids.ids + self.partner_vendor_strategy_validator_ids.ids)]
        self.env.ref('ges_logistics_application_partner.group_partner_application_user_approve').users = [(6, 0, self.partner_kyc_approver_ids.ids + self.partner_crm_approver_ids.ids + self.partner_customer_credit_approver_ids.ids + self.partner_customer_strategy_approver_ids.ids + self.partner_vrm_approver_ids.ids + self.partner_vendor_credit_approver_ids.ids + self.partner_vendor_strategy_approver_ids.ids)]
        self.env.ref('ges_logistics_application_partner.group_partner_application_user_activate').users = [(6, 0, self.partner_kyc_approver_ids.ids + self.partner_crm_approver_ids.ids + self.partner_customer_credit_approver_ids.ids + self.partner_customer_strategy_approver_ids.ids + self.partner_vrm_approver_ids.ids + self.partner_vendor_credit_approver_ids.ids + self.partner_vendor_strategy_approver_ids.ids)]
        self.env.ref('ges_logistics_application_partner.group_partner_application_user_cancel').users = [(6, 0, self.partner_kyc_approver_ids.ids + self.partner_crm_approver_ids.ids + self.partner_customer_credit_approver_ids.ids + self.partner_customer_strategy_approver_ids.ids + self.partner_vrm_approver_ids.ids + self.partner_vendor_credit_approver_ids.ids + self.partner_vendor_strategy_approver_ids.ids)]


        return res


    def get_values(self):    	
        res = super(ResConfigSettings, self).get_values()    	
        with_user = self.env['ir.config_parameter'].sudo()    	
        partner_kyc_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_kyc_submitter_ids')
        partner_kyc_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_kyc_validator_ids')
        partner_kyc_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_kyc_approver_ids')

        partner_crm_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_crm_submitter_ids')
        partner_crm_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_crm_validator_ids')
        partner_crm_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_crm_approver_ids')

        partner_customer_credit_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_credit_submitter_ids')
        partner_customer_credit_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_credit_validator_ids')
        partner_customer_credit_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_credit_approver_ids')

        partner_customer_strategy_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_strategy_submitter_ids')
        partner_customer_strategy_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_strategy_validator_ids')
        partner_customer_strategy_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_customer_strategy_approver_ids')

        partner_vrm_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_vrm_submitter_ids')
        partner_vrm_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_vrm_validator_ids')
        partner_vrm_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_vrm_approver_ids')

        partner_vendor_credit_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_credit_submitter_ids')
        partner_vendor_credit_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_credit_validator_ids')
        partner_vendor_credit_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_credit_approver_ids')

        partner_vendor_strategy_submitter_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_strategy_submitter_ids')
        partner_vendor_strategy_validator_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_strategy_validator_ids')
        partner_vendor_strategy_approver_ids = with_user.get_param('ges_logistics_application_partner.partner_vendor_strategy_approver_ids')



        res.update(
            partner_kyc_submitter_ids=[(6, 0, literal_eval(partner_kyc_submitter_ids))] if partner_kyc_submitter_ids else False,
            partner_kyc_validator_ids=[(6, 0, literal_eval(partner_kyc_validator_ids))] if partner_kyc_validator_ids else False,
            partner_kyc_approver_ids=[(6, 0, literal_eval(partner_kyc_approver_ids))] if partner_kyc_approver_ids else False,

            partner_crm_submitter_ids=[(6, 0, literal_eval(partner_crm_submitter_ids))] if partner_kyc_submitter_ids else False,
            partner_crm_validator_ids=[(6, 0, literal_eval(partner_crm_validator_ids))] if partner_kyc_submitter_ids else False,
            partner_crm_approver_ids=[(6, 0, literal_eval(partner_crm_approver_ids))] if partner_kyc_submitter_ids else False,

            partner_customer_credit_submitter_ids=[(6, 0, literal_eval(partner_customer_credit_submitter_ids))] if partner_customer_credit_submitter_ids else False,
            partner_customer_credit_validator_ids=[(6, 0, literal_eval(partner_customer_credit_validator_ids))] if partner_customer_credit_validator_ids else False,
            partner_customer_credit_approver_ids=[(6, 0, literal_eval(partner_customer_credit_approver_ids))] if partner_customer_credit_approver_ids else False,

            partner_customer_strategy_submitter_ids=[(6, 0, literal_eval(partner_customer_strategy_submitter_ids))] if partner_customer_strategy_submitter_ids else False,
            partner_customer_strategy_validator_ids=[(6, 0, literal_eval(partner_customer_strategy_validator_ids))] if partner_customer_strategy_validator_ids else False,
            partner_customer_strategy_approver_ids=[(6, 0, literal_eval(partner_customer_strategy_approver_ids))] if partner_customer_strategy_approver_ids else False,


            partner_vrm_submitter_ids=[(6, 0, literal_eval(partner_vrm_submitter_ids))] if partner_kyc_submitter_ids else False,
            partner_vrm_validator_ids=[(6, 0, literal_eval(partner_vrm_validator_ids))] if partner_kyc_submitter_ids else False,
            partner_vrm_approver_ids=[(6, 0, literal_eval(partner_vrm_approver_ids))] if partner_kyc_submitter_ids else False,

            partner_vendor_credit_submitter_ids=[(6, 0, literal_eval(partner_vendor_credit_submitter_ids))] if partner_vendor_credit_submitter_ids else False,
            partner_vendor_credit_validator_ids=[(6, 0, literal_eval(partner_vendor_credit_validator_ids))] if partner_vendor_credit_validator_ids else False,
            partner_vendor_credit_approver_ids=[(6, 0, literal_eval(partner_vendor_credit_approver_ids))] if partner_vendor_credit_approver_ids else False,

            partner_vendor_strategy_submitter_ids=[(6, 0, literal_eval(partner_vendor_strategy_submitter_ids))] if partner_vendor_strategy_submitter_ids else False,
            partner_vendor_strategy_validator_ids=[(6, 0, literal_eval(partner_vendor_strategy_validator_ids))] if partner_vendor_strategy_validator_ids else False,
            partner_vendor_strategy_approver_ids=[(6, 0, literal_eval(partner_vendor_strategy_approver_ids))] if partner_vendor_strategy_approver_ids else False,

            )    	
        return res