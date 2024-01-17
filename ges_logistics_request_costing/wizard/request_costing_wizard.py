# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class CMORW(models.TransientModel):
    _name = 'cmo.request.wizard'


    wizard_type = fields.Selection([('new','New'),('update','Update')], string="Wizard Type")
    request_id = fields.Many2one('request.costing',string="Request")
    so_line_id = fields.Many2one('sale.order.line', string="SO Line")
    currency_id = fields.Many2one(related='so_line_id.currency_id', depends=['so_line_id.currency_id'], store=True, string='Currency')

    so_id = fields.Many2one('sale.order', string="Sale Order", related="so_line_id.order_id")
    product_id = fields.Many2one('product.product', string="Product", related="so_line_id.product_id")

    target_cost = fields.Monetary("Target Cost", digits=2, tracking=True, default=0)
    target_date = fields.Datetime("Deadline", default=fields.Datetime.now())
    request_notes = fields.Html('Request Notes', tracking=True)
    
    exitem_ids = fields.One2many('cmow.request.exitem', 'cmorw_id', string="Vendor(s)")
    initem_ids = fields.One2many('cmow.request.initem', 'cmorw_id', string="Internal Item(s)")

    assigned_user_id = fields.Many2one('res.users', string="Assigned Buyer", compute="_compute_main_user_team", store=True, readonly=False, index=True,)
    assigned_ou_id = fields.Many2one('operating.unit', string="Assigned Unit", related="assigned_user_id.default_operating_unit_procurement_id")

    @api.depends('product_id','exitem_ids','initem_ids')
    @api.onchange('product_id','exitem_ids','initem_ids')
    def _compute_main_user_team(self):
        for record in self:
            if not(record.exitem_ids or record.initem_ids) and record.product_id and not (record._origin.id and record.assigned_user_id):
                record.assigned_user_id = record.product_id.procurement_user_id

    def confirm_action(self):
        for record in self:
            if record.wizard_type == 'new':
                exitems = []
                for item in record.exitem_ids:
                    exitem = {
                        'type':'external',
                        'vendor_id':item.vendor_id.id,
                        'assigned_user_id':item.assigned_user_id.id if item.assigned_user_id else record.assigned_user_id.id,
                        'requested': True,

                    }
                    exitems.append((0, None, exitem))
                
                initems = []
                for item in record.initem_ids:
                    initem = {
                        'type':'internal',
                        'product_id':item.product_id.id,
                        'quantity':item.quantity,
                        'product_uom':item.product_uom.id,
                        'assigned_user_id':item.assigned_user_id.id if item.assigned_user_id else record.assigned_user_id.id,
                        'requested': True,
                    }
                    initems.append((0, None, initem))

                
                lines_dict = {
                    'so_line_id': record.so_line_id.id,
                    'target_cost': record.target_cost,
                    'target_date': record.target_date,
                    'request_notes': record.request_notes,
                    'assigned_user_id': record.assigned_user_id.id,
                    'request_item_ids': exitems + initems,
                    }
                    
                newrec = record.env['request.costing'].create(lines_dict)
                
                record.so_line_id.request_costing_id = newrec.id
                
                result = {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'request.costing',
                    'target': 'current',
                    'res_id': newrec.id,
                    'domain': [],
                } 
                return result 

            elif record.wizard_type == 'update':
                exitems = []
                for item in record.exitem_ids:
                    exitem = {
                        'type':'external',
                        'vendor_id':item.vendor_id.id,
                        'assigned_user_id':item.assigned_user_id.id if item.assigned_user_id else record.assigned_user_id.id,
                        'requested': True if record.request_id.state == 'draft' else False,
                    }
                    exitems.append((0, None, exitem))
                
                initems = []
                for item in record.initem_ids:
                    initem = {
                        'type':'internal',
                        'product_id':item.product_id.id,
                        'quantity':item.quantity,
                        'product_uom':item.product_uom.id,
                        'assigned_user_id':item.assigned_user_id.id if item.assigned_user_id else record.assigned_user_id.id,
                        'requested': True if record.request_id.state == 'draft' else False,
                    }
                    initems.append((0, None, initem))
                
                record.request_id.update({
                    'request_item_ids': exitems + initems,
                })



class CMORWExItem(models.TransientModel):
    _name = 'cmow.request.exitem'

    cmorw_id = fields.Many2one('cmo.request.wizard')
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    assigned_user_id = fields.Many2one(comodel_name='res.users',string="Assigned To",compute='_compute_assigned_user_id',store=True, readonly=False, index=True,)
    assigned_ou_id = fields.Many2one(comodel_name='operating.unit', string="Assigned Unit", related='assigned_user_id.default_operating_unit_procurement_id', store=True) 

    @api.depends('vendor_id')
    @api.onchange('vendor_id')
    def _compute_assigned_user_id(self):
        for record in self:
            if record.vendor_id and not (record._origin.id and record.assigned_user_id):
                record.assigned_user_id = record.vendor_id.procurement_user_id or record.assigned_user_id

class CMORWInItem(models.TransientModel):
    _name = 'cmow.request.initem'

    cmorw_id = fields.Many2one('cmo.request.wizard')
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Integer("Quantity", default="1")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', depends=['product_id'])
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        compute='_compute_product_uom',
        store=True, readonly=False, precompute=True, ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]") 
    
    assigned_user_id = fields.Many2one(comodel_name='res.users',string="Assigned To",compute='_compute_assigned_user_id',store=True, readonly=False, index=True,)
    assigned_ou_id = fields.Many2one(comodel_name='operating.unit', string="Assigned Unit", related='assigned_user_id.default_operating_unit_procurement_id', store=True) 

    @api.depends('product_id')
    def _compute_product_uom(self):
        for line in self:
            if not line.product_uom or (line.product_id.uom_id.id != line.product_uom.id):
                line.product_uom = line.product_id.uom_id
                
    @api.depends('product_id')
    @api.onchange('product_id')
    def _compute_assigned_user_id(self):
        for record in self:
            if record.product_id and not (record._origin.id and record.assigned_user_id):
                record.assigned_user_id = record.product_id.procurement_user_id or record.assigned_user_id