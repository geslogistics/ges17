# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import re

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


class LogisticsFreightMoveType(models.Model):
    _name = 'logistics.freight.move.type'
    _description = 'Move Types'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    code = fields.Char(string='Code')
    name = fields.Char(string='Name')




class ShipmentPackageLine(models.Model):
    _name = 'logistics.shipment.package.line'
    _description = 'Freight Package Line'
    _rec_name = 'package'

    name = fields.Char(string='Container Number', required=True)
    package_type = fields.Selection([('item', 'Box / Cargo'), ('container', 'Container / Box')], string="Package Type")
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('road', 'Road'),('rail','Rail')]), string='Transport')
    shipment_id = fields.Many2one('logistics.shipment.order', 'Shipment ID')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    package = fields.Many2one('logistics.freight.package', string='Size / Package', required=True)
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer'), ('flat_rock', 'Flat Rock'), ('open_top', 'Open Top'),
          ('other', 'Other')]), string="Type ")
    qty = fields.Float('Qty', required=True, default=1.0)
    harmonize = fields.Char('Harmonize')
    temperature = fields.Char('Temperature')
    humidity = fields.Char(string="Humidity")
    ventilation = fields.Char(string="Ventilation")
    vgm = fields.Char('VGM', help='Verified gross mass')
    carrier_seal = fields.Char('Carrier Seal')
    seal_number = fields.Char('Seal Number')
    reference = fields.Char('Reference')
    dangerous_goods = fields.Boolean('Dangerous Goods')
    class_number = fields.Char('Class Number')
    un_number = fields.Char('UN Number')
    Package_group = fields.Char('Packaging Group:')
    imdg_code = fields.Char('IMDG Code', help='International Maritime Dangerous Goods Code')
    flash_point = fields.Char('Flash Point')
    material_description = fields.Text('Material Description')
    freight_item_lines = fields.One2many('logistics.shipment.item', 'package_line_id')
    route_id = fields.Many2one('freight.route', 'Route')
    container_type = fields.Selection(
        [('GP', 'GP (General Purpose)'), ('HC', 'HC (High Cube)'),
         ('RF', 'RF (Reefer)'), ('FR', 'FR (Flat Rack)'),
         ('OT', 'OT (Open Top)'), ('GOH', 'GOH (Garment of Hanger)')], string="Type", default="GP")
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    net_weight = fields.Float(string="Net Weight (KG)")
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('name')
    def container_no_check_onchange(self):
        for rec in self:
            if rec.name:
                if len(rec.name) > 11:
                    raise ValidationError(
                        f"The container number exceeds the maximum length (11 characters): {rec.name}"
                    )
                if not re.match('^[A-Z]{4}[0-9]{7,}$', rec.name.upper()):
                    raise ValidationError(
                        f"You have Entered a Wrong Container Number or Format: {rec.name.upper()}\n"
                        "Format is ABCD1234567\n"
                        "First Four Characters Must be Alphabet and Last Seven Characters Must be Numeric"
                    )
                rec.name = rec.name.upper()

    @api.onchange('package')
    def _onchange_package_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.metric_volume
                rec.gross_weight = rec.package.metric_gross_weight
                rec.height = rec.package.metric_height
                rec.length = rec.package.metric_length
                rec.width = rec.package.metric_width

    @api.onchange('package', 'package_type')
    def onchange_package_id(self):
        for line in self:
            if line.package_type == "item":
                if line.shipment_id.transport == 'air':
                    return {'domain': {'package': [('air', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'ocean':
                    return {'domain': {'package': [('ocean', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'road':
                    return {'domain': {'package': [('road', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'rail':
                    return {'domain': {'package': [('rail', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            elif line.package_type == "container":
                if line.shipment_id.transport == 'air':
                    return {
                        'domain': {'package': [('air', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'ocean':
                    return {
                        'domain': {'package': [('ocean', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'road':
                    return {
                        'domain': {'package': [('road', '=', True), ('is_container', '=', True), ('active', '=', True)]}}
                if line.shipment_id.transport == 'rail':
                    return {
                        'domain': {'package': [('rail', '=', True), ('is_container', '=', True), ('active', '=', True)]}}


class ShipmentItem(models.Model):
    _name = 'logistics.shipment.item'
    _description = 'Shipment Item Line'

    name = fields.Char(string='Description')
    package_line_id = fields.Many2one('logistics.shipment.package.line', 'Shipment ID')
    package = fields.Many2one('logistics.freight.package', 'Item')
    type = fields.Selection(
        ([('dry', 'Dry'), ('reefer', 'Reefer')]), string="Operation")
    qty = fields.Float('Qty', default=1.0)
    # Dimension
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    height = fields.Float(string='Height(cm)')
    length = fields.Float(string='Length(cm)')
    width = fields.Float(string='Width(cm)')

    @api.onchange('package')
    def onchange_package_id(self):
        for line in self:
            if line.package_line_id.shipment_id.transport == 'air':
                return {'domain': {'package': [('air', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_id.transport == 'ocean':
                return {'domain': {'package': [('ocean', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_id.transport == 'road':
                return {'domain': {'package': [('road', '=', True), ('is_item', '=', True), ('active', '=', True)]}}
            if line.package_line_id.shipment_id.transport == 'rail':
                return {'domain': {'package': [('rail', '=', True), ('is_item', '=', True), ('active', '=', True)]}}

    @api.onchange('package')
    def _onchange_item_dimension(self):
        for rec in self:
            if rec.package:
                rec.volume = rec.package.metric_volume
                rec.gross_weight = rec.package.metric_gross_weight
                rec.height = rec.package.metric_height
                rec.length = rec.package.metric_length
                rec.width = rec.package.metric_width
                rec.name = rec.package.desc