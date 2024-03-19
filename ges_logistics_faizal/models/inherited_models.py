# -*- coding: utf-8 -*-

from odoo import models, api, tools, fields, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    shipper = fields.Boolean('Shipper')
    consignee = fields.Boolean('Consignee')
    agent = fields.Boolean('Agent')
    is_policy = fields.Boolean('Policy Company')
    vendor = fields.Boolean(string="Vendor")
    notify = fields.Boolean(string="Notify")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    jobs_pending_warning = fields.Text(compute='_compute_jobs_pending_warning')

    def _compute_jobs_pending_warning(self):
        pending_job_orders = []
        for line in self.order_line:
            if line.reference_document and line.reference_document._name == 'logistics.customs.order':
                for doc in line.reference_document:
                    if doc.state != 'clearance_completed':
                        pending_job_orders.append(doc)
            if line.reference_document and line.reference_document._name == 'logistics.transport.order':
                for doc in line.reference_document:
                    if doc.state != 'delivery_completed':
                        pending_job_orders.append(doc)

        if pending_job_orders:
            pending_list = '\n- '.join([order.name for order in pending_job_orders])
            message = (f"""Caution: The job orders listed below remain outstanding.\n- {pending_list}""")
            self.jobs_pending_warning = message
        else:
            self.jobs_pending_warning = ''

    # def action_confirm(self):
    #     for rec in self:
    #         if self.partner_id.partner_state != 'approved':
    #             raise UserError(_('You can not confirm this order as customer is not approved!'))
    #     return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # adjust fields

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        ondelete='restrict', string="Source Document", tracking=True)

    def initiate_reference_document(self):
        # self.reference_document = '%s,%s'% ('logistics.shipment.order',self.env['logistics.shipment.order'].create({}).id)

        if self.product_template_id:
            if self.product_template_id.sale_order_line_workflow == 'shipment':
                newsh = self.env['logistics.shipment.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.shipment.order', newsh.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Shipment Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.shipment.order',
                    'res_id': newsh.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'transport':

                newtr = self.env['logistics.transport.order'].create({'partner_id': self.order_id.partner_id.id, })
                self.reference_document = '%s,%s' % ('logistics.transport.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Transport Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.transport.order',
                    'res_id': newtr.id,
                    'target': 'self',
                }

            elif self.product_template_id.sale_order_line_workflow == 'storage':

                newtr = self.env['logistics.storage.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.storage.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Storage Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.storage.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'customs':

                newtr = self.env['logistics.customs.order'].create({
                    'partner_id': self.order_id.partner_id.id,
                    'so_id': self.order_id.id,
                })
                self.reference_document = '%s,%s' % ('logistics.customs.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Customs Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.customs.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'service':

                newtr = self.env['logistics.service.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.service.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Service Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.service.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

    def select_reference_document(self):
        if self.product_template_id:
            if self.product_template_id.sale_order_line_workflow == 'shipment':
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Shipment Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.shipment.order',
                    'res_id': newsh.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'transport':

                newtr = self.env['logistics.transport.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.transport.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Transport Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.transport.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'storage':

                newtr = self.env['logistics.storage.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.storage.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Storage Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.storage.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'customs':

                newtr = self.env['logistics.customs.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.customs.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Customs Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.customs.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }

            elif self.product_template_id.sale_order_line_workflow == 'service':

                newtr = self.env['logistics.service.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.service.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Service Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.service.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }


class ProductCategory(models.Model):
    _inherit = ['product.category']

    sale_order_line_workflow = fields.Selection([
        ('shipment', 'Shipment'),
        ('transport', 'Transportation'),
        ('service', 'Service'),
        ('storage', 'Storage'),
        ('customs', 'Customs'),
    ], string="Selling Workflow", copy=True, tracking=True)


class Product(models.Model):
    _inherit = ['product.template']

    # adjust fields
    is_logistics = fields.Boolean("Is Logistics")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group")
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type",
                                      domain="[('product_group_id','=',product_group_id)]")
    shipment_mode_id = fields.Many2one('logistics.product.shipment.type', string="Shipment Type",
                                       domain="[('freight_type_id','=',freight_type_id),('product_group_id','=',product_group_id)]")
    sale_order_line_workflow = fields.Selection(
        [('shipment', 'Shipment'), ('transport', 'Transportation'), ('service', 'Service'), ('storage', 'Storage'), ('customs', 'Customs'), ],
        string="Selling Workflow", copy=True, tracking=True)
    # Product Group Type Defined Here
    product_group_type = fields.Selection(
        [('customs', 'Customs'), ('transport', 'Transportation'), ('shipment', 'Shipment'), ('warehouse', 'Warehouse')], string="Product Group Type",
        tracking=True)


class ProductGroup(models.Model):
    _name = "logistics.product.product.group"

    name = fields.Char(string="Group Name", required=True, copy=True, tracking=True)
    product_group_category = fields.Selection(
        [('freight', 'Freight'), ('warehousing', 'Warehousing'), ('service', 'Service'), ('others', 'Others')],
        default="freight", string='Product Group Category', required=True, copy=True, tracking=True)


class FreightType(models.Model):
    _name = "logistics.product.freight.type"

    name = fields.Char(string="Freight Type Name", required=True, copy=True, tracking=True)
    freight_type_category = fields.Selection(
        [('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('others', 'Others')],
        default="ocean", string='Freight Type Category', required=True, copy=True, tracking=True)
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group")
    # product_group_category = fields.Char('Product Group Category', related="product_group_id.product_group_category")


class ShipmentType(models.Model):
    _name = "logistics.product.shipment.type"

    name = fields.Char(string="Shipment Type Name", required=True, copy=True, tracking=True)
    shipment_mode_category = fields.Selection(
        [('full', 'Full Load'), ('less', 'Less Than Load'), ('others', 'Others')],
        default="full", string='Shipment Type Category', required=True, copy=True, tracking=True)
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group",
                                       related='freight_type_id.product_group_id')
    # freight_type_category = fields.Char('Freight Type Category', related="freight_type_id.freight_type_category")


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    truck_current_status = fields.Selection(string='Truck Current Status', tracking=True,
                                            selection=[('idle', 'Idle'), ('under_maintenance', 'Under Maintenance'), ('accident', 'Accident'),
                                                       ('in_transit', 'In Transit')])
