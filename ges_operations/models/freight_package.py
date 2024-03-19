# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FreightPackage(models.Model):
    _name = 'freight.package'
    _description = 'Freight Package'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name / Size')

    is_container = fields.Boolean('Container/Box')
    is_item = fields.Boolean(string='Is Item')
    other = fields.Boolean('Other')

    air = fields.Boolean(string='Air')
    ocean = fields.Boolean(string='Ocean')
    road = fields.Boolean(string='Road')
    rail = fields.Boolean(string='Rail')

    desc = fields.Char(string="Description")

    unit_type = fields.Selection([('metric', 'Metric'), ('imperial', 'Imperial')])

    metric_height = fields.Float(string='Height (cm)')
    metric_length = fields.Float(string='Length (cm)')
    metric_width = fields.Float(string='Width (cm)')
    metric_volume = fields.Float('Volume (m3)')
    metric_gross_weight = fields.Float('Gross Weight (kg)')

    imperial_height = fields.Float(string='Height (inch)')
    imperial_length = fields.Float(string='Length (inch)')
    imperial_width = fields.Float(string='Width (inch)')
    imperial_volume = fields.Float('Volume (ft3)')
    imperial_gross_weight = fields.Float('Gross Weight (lb)')

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
        recs = self.search(['|', ('name', operator, name), ('code', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(FreightPackage, self).name_search(name=name, args=args, operator=operator, limit=limit)
        return recs.name_get()

