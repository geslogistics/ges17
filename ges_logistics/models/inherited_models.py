# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.sale.models.sale_order_line import SaleOrderLine as OriginalSaleOrderLine
from odoo.addons.purchase.models.purchase_order_line import PurchaseOrderLine as OriginalPurchaseOrderLine
from odoo.fields import Command
from odoo.exceptions import ValidationError, UserError

def _prepare_invoice_line(self, **optional_values):
    """Prepare the values to create the new invoice line for a sales order line.

    :param optional_values: any parameter that should be added to the returned invoice line
    :rtype: dict
    """
    
    self.ensure_one()
    res = {
        'display_type': self.display_type or 'product',
        'sequence': self.sequence,
        'name': self.name,
        'product_id': self.product_id.id,
        'reference_document': ('%s,%s' % (self.reference_document._name, self.reference_document.id)) if self.reference_document else None,
        'product_uom_id': self.product_uom.id,
        'quantity': self.qty_to_invoice,
        'discount': self.discount,
        'price_unit': self.price_unit,
        'tax_ids': [Command.set(self.tax_id.ids)],
        'sale_line_ids': [Command.link(self.id)],
        'is_downpayment': self.is_downpayment,
    }
    analytic_account_id = self.order_id.analytic_account_id.id
    if self.analytic_distribution and not self.display_type:
        res['analytic_distribution'] = self.analytic_distribution
    if analytic_account_id and not self.display_type:
        analytic_account_id = str(analytic_account_id)
        if 'analytic_distribution' in res:
            res['analytic_distribution'][analytic_account_id] = res['analytic_distribution'].get(analytic_account_id, 0) + 100
        else:
            res['analytic_distribution'] = {analytic_account_id: 100}
    if optional_values:
        res.update(optional_values)
    if self.display_type:
        res['account_id'] = False
    return res
OriginalSaleOrderLine._prepare_invoice_line = _prepare_invoice_line

def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type or 'product',
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'reference_document': ('%s,%s' % (self.reference_document._name, self.reference_document.id)) if self.reference_document else None,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'purchase_line_id': self.id,
        }
        if self.analytic_distribution and not self.display_type:
            res['analytic_distribution'] = self.analytic_distribution
        return res
OriginalPurchaseOrderLine._prepare_account_move_line = _prepare_account_move_line

class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    # adjust fields

    product_id = fields.Many2one(
        context={'display_default_code': False})

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        string="Ref Doc", tracking=True)

    @api.depends('product_template_id')
    @api.onchange('product_template_id')
    def update_ref_doc(self):
        if self.product_template_id.sale_order_line_workflow == 'sho':
            self.reference_document = ('%s,%s' % ('logistics.shipment.order', 1))

    def action_link_ref_doc(self):
        ctx = {"default_sol_id": self.id}
        if self.reference_document:
            if self.reference_document._name == "logistics.shipment.order":
                ctx['default_shipment_order_id'] = self.reference_document.id
            elif self.reference_document._name == "logistics.transport.order":
                ctx['default_transport_order_id'] = self.reference_document.id
            elif self.reference_document._name == "logistics.storage.order":
                ctx['default_storage_order_id'] = self.reference_document.id
            elif self.reference_document._name == "logistics.customs.order":
                ctx['default_customs_order_id'] = self.reference_document.id
            elif self.reference_document._name == "logistics.service.order":
                ctx['default_service_order_id'] = self.reference_document.id

        #raise UserError(str(ctx))
        result = {
            "name": "Reference Document",
            "type": "ir.actions.act_window",
            "res_model": "logistics.wizard.doc.config",
            "view_mode": "form",
            'view_type': 'form',
            "context": ctx,
            'target': 'new'
        }

        return result

    @api.onchange('product_id')
    def clear_ref_doc(self):
        #raise UserError('test')
        self.reference_document = False

class SaleOrder(models.Model):
    _inherit = ['sale.order']
    
    @api.onchange('partner_id')
    def check_linkage_before_change_partner(self):
        for line in self.order_line:
            if line.reference_document:
                if line.reference_document.partner_id != self.partner_id:
                    raise UserError("Cannot change Customer due to linked Ref Doc " + str(line.reference_document.name))


    

class ProductCategory(models.Model):
    _inherit = ['product.category']

    sale_order_line_workflow = fields.Selection([
        ('sho', 'Shipment'),
        ('tro', 'Transportation'),
        ('svo', 'Service'),
        ('sto', 'Storage'),
        ('cco', 'Customs'),
    ], string="Selling Workflow", copy=True, tracking=True)

class ProductProduct(models.Model):
    _inherit = ['product.product']

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name
    

class ProductTemplate(models.Model):
    _inherit = ['product.template']

    # adjust fields
    is_logistics = fields.Boolean("Is Logistics")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group")
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type",
                                      domain="[('product_group_id','=',product_group_id)]")
    shipment_type_id = fields.Many2one('logistics.product.shipment.type', string="Shipment Type",
                                       domain="[('freight_type_id','=',freight_type_id),('product_group_id','=',product_group_id)]")
    
    sale_order_line_workflow = fields.Selection([('sho','Shipment Order'),('tro','Transport Order'),('sto','Storage Order'),('cco','Customs Order'),('svo','Service Order')], string="Ref Doc Type", tracking=True, copy=True)

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

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
    shipment_type_category = fields.Selection(
        [('full', 'Full Load'), ('less', 'Less Than Load'), ('others', 'Others')],
        default="full", string='Shipment Type Category', required=True, copy=True, tracking=True)
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group",
                                       related='freight_type_id.product_group_id')
    # freight_type_category = fields.Char('Freight Type Category', related="freight_type_id.freight_type_category")

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    # add fields

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        ondelete='restrict', string="Ref Doc", tracking=True)


class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']

    # add fields

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        ondelete='restrict', string="Ref Doc", tracking=True)
    