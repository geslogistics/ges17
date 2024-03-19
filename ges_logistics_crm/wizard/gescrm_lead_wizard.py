# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from ast import literal_eval

class GESCRMLeadWizard(models.TransientModel):
    _name = 'gescrm.lead.wizard'

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)

    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )


    ## COMMON KYC FIELDS
    company_type = fields.Selection(string='Company Type', selection=[('company', 'Company'),('person', 'Individual')], default="company")
    legal_name = fields.Char(string='Name', help="Official / Legal English Name")
    name_alt_lang = fields.Char(string='Name (AR)', help="Official / Legal Name (AR)")
    trade_name = fields.Char(string='Trading Name', translate=True, help="if different from Legal Entity Name")
    trade_name_alt_lang = fields.Char(string='Trading Name (AR)', translate=True, help="if different from Legal Entity Name")
    
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    email = fields.Char()
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)
    website = fields.Char('Website Link')
    company_registry = fields.Char(string="CR/ID Number", help="The official CR/ID number. Use it if it is different from the Tax ID. It must be unique across all partners of a same country")
    vat = fields.Char(string='Tax ID', help="i.e. VAT Number")


    possible_partner_ids = fields.Many2many("res.partner", "partner_possible_lead", "partner_lead_id", "lead_partner_id", string="Possible Accounts")



    
    def find_accounts(self):
        for partner in self.sudo():

            pids = []
            
            #clear possible partners
            
            #record.partner_id.active_application_ids = [(3, current_active_application.id)]

            Partner = self.with_context(active_test=False).env['res.partner'].sudo()

            odomain = [
                ('parent_id','=',False),
            ]
            if partner.company_id:
                odomain += [('company_id', 'in', [False, partner.company_id.id])]

            # check vat
            domain = odomain + [
                ('vat', '=', partner.vat), 
                ('country_id','=',partner.country_id.id),
            ]
            should_check_vat = partner.vat and len(partner.vat) != 1
            #partner.same_pa_vat_partner_id = should_check_vat and Partner.search(domain, limit=1)
            if should_check_vat:
                pids.append(Partner.search(domain).ids)
            
            
            # check company_registry
            domain = odomain + [
                ('company_registry', '=', partner.company_registry),
                ('country_id','=',partner.country_id.id),
            ]
            #partner.same_pa_company_registry_partner_id = bool(partner.company_registry) and Partner.search(domain, limit=1)
            if bool(partner.company_registry):
                pids.append(Partner.search(domain).ids)
            

            # check name
            domain = odomain + [
                ('name','ilike',partner.legal_name),
                
            ]
            #partner.same_pa_name_partner_id = bool(partner.legal_name) and Partner.search(domain, limit=1)
            if bool(partner.legal_name):
                pids.append(Partner.search(domain).ids)

            # check website
            domain = odomain + [
                ('website', '=', partner.website),
            ]
            #partner.same_pa_website_partner_id = bool(partner.website) and Partner.search(domain, limit=1)
            if bool(partner.website):
                pids.append(Partner.search(domain).ids)

            # check email
            domain = odomain + [
                ('email', '=', partner.email),
            ]
            #partner.same_pa_email_partner_id = bool(partner.email) and Partner.search(domain, limit=1)
            if bool(partner.email):
                pids.append(Partner.search(domain).ids)

            # check phone
            domain = odomain + [
                ('phone', '=', partner.phone),
                ('country_id','=',partner.country_id.id),
            ]
            #partner.same_pa_phone_partner_id = bool(partner.phone) and Partner.search(domain, limit=1)
            if bool(partner.phone):
                pids.append(Partner.search(domain).ids)

            # check mobile
            domain = odomain + [
                ('mobile', '=', partner.mobile),
                ('country_id','=',partner.country_id.id),
            ]
            #partner.same_pa_mobile_partner_id = bool(partner.mobile) and Partner.search(domain, limit=1)
            if bool(partner.mobile):
                pids.append(Partner.search(domain).ids)
       
            if pids:
                log = ",".join(str(x) for x in pids)
                #raise UserError(log)
                partner.possible_partner_ids = [(6, 0, literal_eval(log))]

            cur_id = self.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'gescrm.lead.wizard',
                'res_id': cur_id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                    }