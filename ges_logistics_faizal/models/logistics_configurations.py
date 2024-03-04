# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class LogisticsFreightAddressContinent(models.Model):
    _name = 'logistics.freight.address.continent'
    _description = 'Logistics Continent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)


class LogisticsFreightAddressRegion(models.Model):
    _name = 'logistics.freight.address.region'
    _description = 'Logistics Region'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    continent_ids = fields.Many2many('logistics.freight.address.continent', 'region_continent', string="Continent(s)",
                                     tracking=True, ondelete='restrict')


class LogisticsFreightAddressCountry(models.Model):
    _name = 'logistics.freight.address.country'
    _description = 'Logistics Country'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code2 = fields.Char(string='ISO Alpha2-Code', tracking=True)
    code = fields.Char(string='ISO Alpha3-Code', tracking=True)
    continent_id = fields.Many2one('logistics.freight.address.continent', string="Continent", tracking=True,
                                   ondelete='restrict')
    region_ids = fields.Many2many('logistics.freight.address.region', 'country_region', string="Region(s)",
                                  tracking=True, ondelete='restrict')
    country_call_code = fields.Integer(string='Country Calling Code', tracking=True)

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressCountry, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressCountry, self).name_search(name=name, args=args, operator=operator,
                                                                           limit=limit)
        return recs.name_get()


class LogisticsFreightAddressState(models.Model):
    _name = 'logistics.freight.address.state'
    _description = 'Logistics State'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressState, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressState, self).name_search(name=name, args=args, operator=operator,
                                                                         limit=limit)
        return recs.name_get()


class LogisticsFreightAddressCity(models.Model):
    _name = 'logistics.freight.address.city'
    _description = 'Freight City'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State",
                               domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressCity, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressCity, self).name_search(name=name, args=args, operator=operator,
                                                                        limit=limit)
        return recs.name_get()


class LogisticsFreightAddress(models.Model):
    _name = 'logistics.freight.address'
    _description = 'Logistics Address'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

    partner_id = fields.Many2one('res.partner', string="Partner", tracking=True, ondelete='cascade')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    # Address
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State",
                               domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')
    city_id = fields.Many2one('logistics.freight.address.city', string="City",
                              domain="[('country_id', '=', country_id),('state_id', '=', state_id)]", tracking=True,
                              ondelete='restrict')
    zip_code = fields.Char(string='Zip Code', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street 2', tracking=True)
    street3 = fields.Char(string='Street 3', tracking=True)
    # Location URL
    location_url = fields.Char(string='Location URL', tracking=True)

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddress, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddress, self).name_search(name=name, args=args, operator=operator,
                                                                    limit=limit)
        return recs.name_get()


class LogisticsFreightAirCarriers(models.Model):
    _name = 'logistics.freight.air.carriers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Air Freight Carriers'

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The code must be unique, this one is already in the system.'),
        ('unique_name', 'UNIQUE(name)', 'The name must be unique, this one is already in the system.')
    ]

    code = fields.Char(string='Code', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    note = fields.Text(string="Notes", tracking=True)


class LogisticsFreightIncoterms(models.Model):
    _name = 'logistics.freight.incoterms'
    _description = 'Freight Incoterms'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    code = fields.Char(string='Code')
    name = fields.Char(string='Name',
                       help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    option_import = fields.Boolean(string="Import")
    option_export = fields.Boolean(string="Export")
    option_ocean = fields.Boolean(string="Ocean")
    option_air = fields.Boolean(string="Air")
    option_rail = fields.Boolean(string="Rail")
    option_road = fields.Boolean(string="Road")
    option_pickup = fields.Boolean(string="Pick-Up")
    option_delivery = fields.Boolean(string="Delivery")
    description = fields.Text(string="Description")


class LogisticsFreightPackage(models.Model):
    _name = 'logistics.freight.package'
    _description = 'Freight Packages'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

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


class LogisticsFreightPort(models.Model):
    _name = 'logistics.freight.port'
    _description = 'Logistics Port'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    air = fields.Boolean(string='Air', tracking=True)
    ocean = fields.Boolean(string='Ocean', tracking=True)
    road = fields.Boolean(string='Road', tracking=True)
    rail = fields.Boolean(string='Rail', tracking=True)
    # Address
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State",
                               domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')
    city_id = fields.Many2one('logistics.freight.address.city', string="City",
                              domain="[('country_id', '=', country_id),('state_id', '=', state_id)]", tracking=True,
                              ondelete='restrict')
    zip_code = fields.Char(string='Zip Code', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street 2', tracking=True)
    street3 = fields.Char(string='Street 3', tracking=True)

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = "[" + record.code + "] " + record.name
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightPort, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(
            ['|', '|', ('code', operator, name), ('name', operator, name), ('city_id', operator, name)] + args,
            limit=limit)
        if not recs.ids:
            return super(LogisticsFreightPort, self).name_search(name=name, args=args, operator=operator, limit=limit)
        return recs.name_get()
