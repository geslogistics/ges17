# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FreightAddress(models.Model):
    _name = 'freight.address'
    _description = 'Freight Address'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

    partner_id = fields.Many2one('res.partner', string="Partner", tracking=True, ondelete='cascade')
    universal_address = fields.Boolean(string="Universal Address")
    is_partner_visible = fields.Boolean(store=False, default=True)

    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
        
    # Address
    country_id = fields.Many2one('res.country', string="Country", tracking=True, ondelete='restrict')
    state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')
    city_id = fields.Many2one('res.city', string="City", domain="[('country_id', '=', country_id),('state_id', '=', state_id)]", tracking=True, ondelete='restrict')
    zip_code = fields.Char(string='Zip Code', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street 2', tracking=True)

    display_name = fields.Char(compute="_compute_display_name")
    def _compute_display_name(self):
        for record in self:
            if record.code:
                record.display_name = "[" + record.code + "] " + record.name
            else:
                record.display_name = record.name

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', '|', '|', ('country_id', operator, name), ('code', operator, name), ('name', operator, name), ('city_id', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(FreightAddress, self).name_search(name=name, args=args, operator=operator,
                                                                    limit=limit)
        return recs.name_get()