from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class CostingMemo(models.Model):
    _name = "costing.memo"
    _description = "Costing Memo"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #check user
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    current_sale_team_id = fields.Many2one('crm.team', string='Sales Team', related="current_user_id.sale_team_id")
    current_purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team', related="current_user_id.purchase_team_id")
    is_pa_user = fields.Boolean(string="Is PA User", compute="_compute_is_pa_user", store=False)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_pa_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_partner.group_partner_application_user_own_docs')
    

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    color = fields.Integer('Color')
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now())
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict', related="so_line_id.order_id.partner_id")
    user_id = fields.Many2one('res.users', string='Create User', index=True, default=lambda self: self.env.user)
    
    sale_user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        related='partner_id.user_id',
        store=True)
    
    sale_team_id = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
        related='partner_id.team_id',
        store=True)    

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='so_id.currency_id', depends=['so_id.currency_id'], store=True, string='Currency')

    buyer_id = fields.Many2one(
        comodel_name='res.users',
        string="Buyer",
        compute='_compute_buyer_id',
        store=True, readonly=False, index=True,
        )
    
    purchase_team_id = fields.Many2one(
        comodel_name='purchase.team',
        string="Purchase Team",
        compute='_compute_purchase_team_id',
        store=True, readonly=False, index=True,
        )

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _compute_buyer_id(self):
        for record in self:
            if record.partner_id and not (record._origin.id and record.buyer_id):
                record.buyer_id = record.partner_id.buyer_id

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def _compute_purchase_team_id(self):
        for record in self:
            if record.partner_id and not (record._origin.id and record.purchase_team_id):
                record.purchase_team_id = record.partner_id.purchase_partner_team_id

    assign_datetime = fields.Datetime(string='Assigned Date')

    so_line_id = fields.Many2one('sale.order.line', string="SO Line")
    so_id = fields.Many2one('sale.order', string="Sale Order", related="so_line_id.order_id")
    product_id = fields.Many2one('product.product', string="Product", related="so_line_id.product_id")

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        string="Ref Doc", related="so_line_id.reference_document")

    


    reference_document_type = fields.Selection([('sho','Shipment Order'),('tro','Transport Order'),('sto','Storage Order'),('cco','Customs Order'),('svo','Service Order')], string="Ref Doc Type", compute="_get_reference_document_type")

    operating_unit_income = fields.Monetary("Operating Unit Income", digits=2, tracking=True, default=0)
    total_costing = fields.Monetary("Total Costing", digits=2, compute='_get_total_costing')

    # request fields
    request_vendor_ids = fields.Many2many('res.partner','prt_id_request_partner_ids', string="Requested Vendor(s)")
    request_notes = fields.Html('Request Notes', tracking=True)

    # offer fields
    offer_vendor_ids = fields.Many2many('res.partner','prt_id_offer_partner_ids', string="Offered Vendor(s)", compute="_get_po_summary")
    offer_notes = fields.Html('Offer Notes', tracking=True)

    # vendor purchase order fields
    po_ids = fields.Many2many('purchase.order', string='Purchases', copy=False, compute="_get_po_ids")
    po_ids_count = fields.Integer("Count of POs", compute='_get_po_ids')
    po_ids_amount_untaxed = fields.Monetary("Purchases Untaxed", digits=2, compute='_get_po_ids')
    po_ids_amount_tax = fields.Monetary("Purchases Taxes", digits=2, compute='_get_po_ids')
    po_ids_amount_total = fields.Monetary("Purchases Total", digits=2, compute='_get_po_ids')
    

    # services received fields
    pol_ids = fields.Many2many('purchase.order.line', string='Purchases', copy=False, compute="_get_pol_ids")
    pol_ids_count = fields.Integer("Count of Services Received", compute='_get_pol_ids')
    pol_ids_amount_untaxed = fields.Monetary("Services Received Untaxed", digits=2, compute='_get_pol_ids')
    pol_ids_amount_tax = fields.Monetary("Services Received Taxes", digits=2, compute='_get_pol_ids')
    pol_ids_amount_total = fields.Monetary("Services Received Total", digits=2, compute='_get_pol_ids')

    #quotations fields
    

    
    

    lowest_po_id = fields.Many2one('purchase.order', string='Lowest PO', compute="_get_po_summary")
    lowest_vendor = fields.Many2one('res.partner', string="Lowest Vendor", related="lowest_po_id.partner_id")
    lowest_po_amount_total = fields.Monetary(string='Lowest Price', compute="_get_po_summary")

    average_po_amount_total = fields.Monetary(string='Average Price', compute="_get_po_summary")

    highest_po_id = fields.Many2one('purchase.order', string='Highest PO', compute="_get_po_summary")
    highest_vendor = fields.Many2one('res.partner', string="Highest Vendor", related="highest_po_id.partner_id")
    highest_po_amount_total = fields.Monetary(string='Highest Price', compute="_get_po_summary")
    
    suggested_po_id = fields.Many2one('purchase.order', string='Suggested PO')
    suggested_vendor = fields.Many2one('res.partner', string="Suggested Vendor", related="suggested_po_id.partner_id")
    suggested_po_amount_total = fields.Monetary(string='Suggested Price', compute="_get_po_summary")
    
    selected_po_id = fields.Many2one('purchase.order', string='Selected PO', tracking=True)
    selected_vendor = fields.Many2one('res.partner', string="Selected Vendor", related="selected_po_id.partner_id")
    selected_po_amount_total = fields.Monetary(string='Selected Price', compute="_get_po_summary")
    


    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            values['name'] = "PRT" + self.env['ir.sequence'].next_by_code('costing.memo') or _('New')
        result = super(CostingMemo, self).create(values)
        
        if values.get('so_line_id', False):
            self.env['sale.order.line'].search([('id','=',values.get('so_line_id', False))]).write({'costing_memo_id':result.id})
        
        return result

    #def write(self, values):
    #    if values.get('name', ('New')) == ('New'):
    #        values['name'] = "PRT" + self.env['ir.sequence'].next_by_code('costing.memo') or _('New')
    #    result = super(CostingMemo, self).write(values)
    #    return result

    def unlink(self):
        for record in self:
            currentrec = str('%s,%s' % (record._name, record.id))
            
            so_ids = record.env['sale.order.line'].search([('reference_document', '=', currentrec)])
            po_ids = record.env['purchase.order.line'].search([('reference_document', '=', currentrec)])
            invoice_ids = record.env['account.move.line'].search([('reference_document', '=', currentrec)]).filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
            bill_ids = record.env['account.move.line'].search([('reference_document', '=', currentrec)]).filtered(lambda r: r.move_type in ('in_invoice', 'in_refund'))

            if so_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Sale Order" + str([so_ids.order_id.name])))
            if po_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Purchase Order" + str([po_ids.order_id.name])))
            if invoice_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Customer Invoice" + str([invoice_ids.move_id.name])))
            if bill_ids:
                raise ValidationError(_("You are trying to delete (" + record.name + ") that is referenced to Vendor Bill" + str([bill_ids.move_id.name])))
    
        return super(CostingMemo, self).unlink()

    @api.onchange('po_ids','suggested_po_id','selected_po_id')
    @api.depends('po_ids','suggested_po_id','selected_po_id')
    def _get_po_summary(self):
        for record in self:
            if record.po_ids:
                record.highest_po_id = record.po_ids.sorted(key=lambda r: r.currency_id._convert(r.amount_total,record.currency_id), reverse=True)[0]
                if record.highest_po_id:
                    record.highest_po_amount_total = record.highest_po_id.currency_id._convert(record.highest_po_id.amount_total,record.currency_id)
                else:
                    record.highest_po_amount_total = 0
                
                record.lowest_po_id = record.po_ids.sorted(key=lambda r: r.currency_id._convert(r.amount_total,record.currency_id))[0]
                if record.lowest_po_id:
                    record.lowest_po_amount_total = record.lowest_po_id.currency_id._convert(record.lowest_po_id.amount_total,record.currency_id)
                else:
                    record.lowest_po_amount_total = 0

                total_po_amounts = sum(po.currency_id._convert(po.amount_total,record.currency_id) for po in record.po_ids.filtered(lambda r: r.amount_total > 0))
                count_positive_po = len(record.po_ids.filtered(lambda r: r.currency_id._convert(r.amount_total,record.currency_id) > 0))
                if count_positive_po:
                    record.average_po_amount_total = total_po_amounts / count_positive_po
                else:
                    record.average_po_amount_total = 0
                record.offer_vendor_ids = record.po_ids.partner_id.ids
            else:
                record.highest_po_id = False
                record.lowest_po_id = False
                record.highest_po_amount_total = 0
                record.average_po_amount_total = 0
                record.lowest_po_amount_total = 0
                record.offer_vendor_ids = False

            
            if record.suggested_po_id:
                record.suggested_po_amount_total = record.suggested_po_id.currency_id._convert(record.suggested_po_id.amount_total,record.currency_id)
            else:
                record.suggested_po_amount_total = 0

            if record.selected_po_id:
                record.selected_po_amount_total = record.selected_po_id.currency_id._convert(record.selected_po_id.amount_total,record.currency_id)
            else:
                record.selected_po_amount_total = 0

            



    @api.onchange('reference_document')
    @api.depends('reference_document')
    def _get_reference_document_type(self):
        for record in self:
            if record.reference_document:
                if record.reference_document._name == "logistics.shipment.order":
                    record.reference_document_type = "sho"
                elif record.reference_document._name == "logistics.transport.order":
                    record.reference_document_type = "tro"
                elif record.reference_document._name == "logistics.storage.order":
                    record.reference_document_type = "sto"
                elif record.reference_document._name == "logistics.customs.order":
                    record.reference_document_type = "cco"
                elif record.reference_document._name == "logistics.service.order":
                    record.reference_document_type = "svo"
            else:
                record.reference_document = False

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            if order.partner_id and not (order._origin.id and order.sale_user_id):
                # Recompute the salesman on partner change
                #   * if partner is set (is required anyway, so it will be set sooner or later)
                #   * if the order is not saved or has no salesman already
                order.sale_user_id = (
                    order.partner_id.user_id
                    or order.partner_id.commercial_partner_id.user_id
                    or (self.user_has_groups('sales_team.group_sale_salesman') and self.env.user)
                )

    @api.depends('partner_id', 'sale_user_id')
    def _compute_team_id(self):
        cached_teams = {}
        for order in self:
            default_team_id = self.env.context.get('default_team_id', False) or order.sale_team_id.id or order.partner_id.team_id.id
            user_id = order.sale_user_id.id
            company_id = order.company_id.id
            key = (default_team_id, user_id, company_id)
            if key not in cached_teams:
                cached_teams[key] = self.env['crm.team'].with_context(
                    default_team_id=default_team_id
                )._get_default_team_id(
                    user_id=user_id, domain=[('company_id', 'in', [company_id, False])])
            order.sale_team_id = cached_teams[key]


    # purchase order functions
    @api.depends('po_ids.prt_id')
    def _get_po_ids(self):
        for record in self:
            purchase_orders = record.env['purchase.order'].sudo().search(
                [('prt_id', '=', record.id)])
            record.po_ids = purchase_orders if purchase_orders else False
            record.po_ids_count = len(purchase_orders) if purchase_orders else False
            record.po_ids_amount_untaxed = sum(line.amount_untaxed for line in purchase_orders) if purchase_orders else False
            record.po_ids_amount_tax = sum(line.amount_tax for line in purchase_orders) if purchase_orders else False
            record.po_ids_amount_total = sum(line.amount_total for line in purchase_orders) if purchase_orders else False

    # purchase order lines (services received) functions
    @api.depends('po_ids')
    def _get_pol_ids(self):
        for record in self:
            purchase_order_lines = record.po_ids.order_line
            record.pol_ids = purchase_order_lines if purchase_order_lines else False
            record.pol_ids_count = len(purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_untaxed = sum(
                line.price_subtotal for line in purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_tax = sum(line.price_tax for line in purchase_order_lines) if purchase_order_lines else False
            record.pol_ids_amount_total = sum(
                line.price_total for line in purchase_order_lines) if purchase_order_lines else False


    def action_view_po(self):
        self.ensure_one()
        result = {
            "name": "Purchase Orders",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [('id', 'in', self.po_ids.ids)],
            "view_mode": "tree,form,search",
            "context": {"create": 0, "delete": 0},
        }
        return result

    def action_create_po(self):
        result = {
            "name": "Purchase Orders",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "context": {"default_prt_id": self.id},
        }
        return result

    
    
    def action_clear_suggest_po(self):
        self.suggested_po_id.suggested_po = 0
        self.suggested_po_id = False
        
    def action_clear_select_po(self):
        self.selected_po_id.selected_po = 0
        self.selected_po_id = False

    @api.depends('selected_po_amount_total','operating_unit_income')
    @api.onchange('selected_po_amount_total','operating_unit_income')
    def _get_total_costing(self):
        self.total_costing = (self.operating_unit_income if self.operating_unit_income else 0) + (self.selected_po_amount_total if self.selected_po_amount_total else 0)

    