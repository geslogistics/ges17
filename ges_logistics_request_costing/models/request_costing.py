from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from ast import literal_eval

class CostingRequest(models.Model):
    _name = "request.costing"
    _description = "Costing Request"
    _inherit = ['mail.thread', 'mail.activity.mixin','user.abstract.mixin']
    
    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids", store=False)
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True, store=False)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True, store=False)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True, store=False)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True, store=False)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True, store=False)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True, store=False)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True, store=False)

    current_operating_unit_sales_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_id", string="Sales Unit", store=False)
    current_operating_unit_sales_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_ops_id", string="Sales Ops Unit", store=False)
    current_operating_unit_procurement_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_id", string="Procurement Unit", store=False)
    current_operating_unit_procurement_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_ops_id", string="Procurement Ops Unit", store=False)
    current_operating_unit_finance_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_id", string="Finance Unit", store=False)
    current_operating_unit_finance_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_ops_id", string="Finance Ops Unit", store=False)
    current_operating_unit_hr_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_hr_id", string="HR Unit", store=False)
    current_operating_unit_it_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_it_id", string="IT Unit", store=False)
    current_operating_unit_marketing_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_marketing_id", string="Marketing Unit", store=False)
    current_operating_unit_executive_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_executive_id", string="Executive Unit", store=False)

    @api.depends("current_user_id", "current_operating_unit_ids")
    def _compute_current_operating_unit_ids(self):
        for user in self:
            user.current_operating_unit_sales_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales')
            user.current_operating_unit_sales_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')
            user.current_operating_unit_procurement_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement')
            user.current_operating_unit_procurement_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')
            user.current_operating_unit_finance_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance')
            user.current_operating_unit_finance_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')
            user.current_operating_unit_hr_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'hr')
            user.current_operating_unit_it_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'it')
            user.current_operating_unit_executive_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'executive')
            user.current_operating_unit_virtual_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'virtual')
    
    is_requester_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_ou_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_ou_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_ou_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_ou_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_user(self):
        self.is_requester_user = self.current_user_id == self.sales_user_id
        self.is_requester_ou_user = self.current_user_id in self.sales_ou_id.user_ids and (self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))
        self.is_requester_ou_manager = self.current_user_id == self.sales_ou_id.manager_id
        self.is_requester_manager = self.env.user.has_group('sales_team.group_sale_manager')
        self.is_requester_any = self.is_requester_user or self.is_requester_ou_user or self.is_requester_ou_manager or self.is_requester_manager
        
        self.is_assigned_user = self.current_user_id in self.assigned_user_ids
        self.is_assigned_ou_user = self.current_user_id in self.assigned_ou_ids.user_ids and (self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))
        self.is_assigned_ou_manager = self.current_user_id in self.assigned_ou_ids.manager_id
        self.is_assigned_manager = self.env.user.has_group('purchase.group_purchase_manager')
        self.is_assigned_any = self.is_assigned_user or self.is_assigned_ou_user or self.is_assigned_ou_manager or self.is_assigned_manager
        
    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    color = fields.Integer('Color')
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')


    state_selections = [
        ('draft', 'Draft'),
        ('sale_validation', 'Sale Validation'),
        ('costing', 'Costing'),
        #('purchase_validation', 'Purchase Validation'),
        ('unsuccessful', 'Unsuccessful'), 
        ('selection', 'Selection'), 
        ('confirmation', 'Confirmation'),
        ('confirmed', 'Confirmed'),
        ('billing', 'Billing'),
        ('billed', 'Billed'),
        ('done', 'Done'), 
        ('cancel', 'Cancelled'),
    ]
    state = fields.Selection(selection=state_selections, default='draft', string='Status')

    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict', related="so_line_id.order_id.partner_id")
    customer_class = fields.Selection([('general','General Account'),('key','Key Account'),('strategic','Strategic Account')], string="Customer Class", related='partner_id.current_crm_id.customer_class')
    customer_segment = fields.Selection([('gov','Government/Semi-Government'),('large','Large Corporates'),('sme','Small & Medium Enterprises'),('retail','Retail')], string="Customer Segment", related='partner_id.current_crm_id.customer_segment')

    sales_user_id = fields.Many2one(
        comodel_name='res.users',
        string="Sales User",
        related='partner_id.sales_user_id',
        store=True)
    
    sales_ou_id = fields.Many2one(
        comodel_name='operating.unit',
        string="Sales Unit",
        related='partner_id.sales_ou_id',
        store=True)    

    requester_user_id = fields.Many2one('res.users', string='Request User', index=True, default=lambda self: self.env.user)
    
    requester_ou_id = fields.Many2one(
        comodel_name='operating.unit',
        string="Request Unit",
        related='requester_user_id.default_operating_unit_sales_id',
        store=True)   

    assigned_user_id = fields.Many2one('res.users', string="Assigned User")
    assigned_ou_id = fields.Many2one('operating.unit', string="Assigned Unit", related="assigned_user_id.default_operating_unit_procurement_id")
    
    assigned_user_ids = fields.Many2many(
        'res.users', 'request_costing_assigned_users',
        string="Assigned User(s)",
        compute='_compute_assigned_user_ids',
        store=True, index=True,
        )
    
    assigned_ou_ids = fields.Many2many(
        'operating.unit', 'request_costing_assigned_units',
        string="Assigned Unit(s)",
        compute='_compute_assigned_user_ids',
        store=True) 

    @api.depends('request_item_ids','assigned_user_id')
    def _compute_assigned_user_ids(self):
        for record in self:
            
            record.assigned_user_ids = record.request_item_ids.assigned_user_id.ids or False
            if record.assigned_user_id:
                record.assigned_user_ids = (([record.assigned_user_id.id] or None) + record.request_item_ids.assigned_user_id.ids) or False
            
            record.assigned_ou_ids = record.assigned_user_ids.default_operating_unit_procurement_id or False
                
                

    #assign_datetime = fields.Datetime(string='Assigned Date')

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

    # request fields
    request_vendor_ids = fields.Many2many('res.partner','request_costing_request_vendor_ids', compute="_compute_request_vendor_ids", string="Requested Vendor(s)")
    request_product_ids = fields.Many2many('product.product','request_costing_request_product_ids', compute="_compute_request_product_ids", string="Requested Product(s)")

    target_cost = fields.Monetary("Target Cost", digits=2, tracking=True, default=0)
    target_date = fields.Datetime("Deadline", tracking=True)
    request_notes = fields.Html('Request Notes')

    # offer fields
    offer_vendor_ids = fields.Many2many('res.partner','request_costing_offer_partner_ids', string="Quoted Vendor(s)", compute="_compute_request_vendor_ids")
    offer_product_ids = fields.Many2many('product.product','request_costing_offer_product_ids', string="Quoted Product(s)", compute="_compute_request_product_ids")
    offer_notes = fields.Html('Offer Notes')
    
    total_in = fields.Monetary(string="Quoted Internal", compute="_compute_items_stats") 
    total_ex = fields.Monetary(string="Quoted External", compute="_compute_items_stats") 
    total_total = fields.Monetary(string="Quoted Total", compute="_compute_items_stats") 

    cost_in = fields.Monetary(string="Cost Internal", compute="_compute_items_stats") 
    cost_ex = fields.Monetary(string="Cost External", compute="_compute_items_stats") 
    cost_total = fields.Monetary(string="Cost Total", compute="_compute_items_stats") 

    @api.depends('request_item_ids.applicable_co_total','request_item_ids.applicable_co_untaxed')
    @api.onchange('request_item_ids.applicable_co_total','request_item_ids.applicable_co_untaxed')
    def _compute_items_stats(self):
        for record in self:
            quoted_item_status = ['quoted','suggested']
            counted_item_status = state_item_selections = ['required','selected','to_confirm','confirmed','to_bill','billed']

            record.total_in = sum(item.applicable_co_total for item in record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.product_id and r.state in quoted_item_status))
            record.total_ex = sum(item.applicable_co_untaxed for item in record.request_item_ids.filtered(lambda r: r.type == 'external' and r.vendor_id and r.state in quoted_item_status))
            record.total_total = record.total_in + record.total_ex

            record.cost_in = sum(item.applicable_co_total for item in record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.product_id and r.state in counted_item_status))
            record.cost_ex = sum(item.applicable_co_untaxed for item in record.request_item_ids.filtered(lambda r: r.type == 'external' and r.vendor_id and r.state in counted_item_status))
            record.cost_total = record.cost_in + record.cost_ex

    def compute_items_stats(self):
        self._compute_items_stats()
        self._update_sol_cost()

    @api.depends('request_item_ids.applicable_co_total','request_item_ids.applicable_co_untaxed')
    @api.onchange('request_item_ids.applicable_co_total','request_item_ids.applicable_co_untaxed')
    def _update_sol_cost(self):
        for record in self:
            record.so_line_id.purchase_price = record.cost_ex

    @api.depends('request_item_ids')
    def _compute_request_vendor_ids(self):
        for record in self:
            record.request_vendor_ids = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.vendor_id and r.requested).vendor_id.ids or False
            record.offer_vendor_ids = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.vendor_id  and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel']).vendor_id.ids or False

    @api.depends('request_item_ids')
    def _compute_request_product_ids(self):
        for record in self:
            record.request_product_ids = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.product_id and r.requested).product_id.ids or False
            record.offer_product_ids = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.product_id and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel']).product_id.ids or False
    
    



    #tickets fields
    ticket_ids = fields.One2many('ticket','request_costing_id', string="Tickets")

    #request items
    request_item_ids = fields.One2many('request.costing.item', 'request_id', string="Items")

    
    @api.model
    def create(self, values):
        if values.get('name', ('New')) == ('New'):
            values['name'] = "CM" + self.env['ir.sequence'].next_by_code('request.costing') or _('New')
        result = super(CostingRequest, self).create(values)
        
 
        return result

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

    

    def action_wizard_submit(self):

        return {
            'name': 'Submit Request(s)',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_submit'
                }
        }

    def _action_submit(self, note=False):
        for record in self:
            record.write({'state': 'sale_validation'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action in ['req_cost_submit','req_cost_resubmit'])
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.id),('state','=','open'),('action','in',['req_cost_submit','req_cost_resubmit'])])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            
            # add pending tickets for team_id team leader
            user_ids = record.requester_ou_id.manager_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_sale',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    #record.write({'ticket_ids': [(0, 0, datas)]})
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #record.offer_notes = str(datas)
                    #record.request_notes = str(new_ticket)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})

            record.compute_items_stats()

    def action_wizard_validate(self):
        
        return {
            'name': 'Validate Request(s)',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_validate'
                }
        }

    def _action_validate(self, note=False):
        for record in self:
            record.write({'state': 'costing'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_sale')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_sale')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket(s) for each requested item's assigned user to request ticket_ids and item ticket_ids

            if record.request_item_ids:
                for item in record.request_item_ids:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'request_costing_item_id': item.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': item.assigned_user_id.id,
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state':'open',
                    }
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #item.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #item.ticket_ids = [(4, new_ticket.id)]
                    #record.ticket_ids = [(4, new_ticket.id)]
            
            else:
                datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': record.assigned_user_id.id,
                        'action':'req_cost_cost',
                        'opened_datetime': fields.Datetime.now(),
                        'state':'open',
                    }
                new_ticket = self.env['ticket'].sudo().create(datas)
            
            record.compute_items_stats()
            

    def action_wizard_return(self):

        return {
            'name': 'Return Request(s)',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_return'
                }
        }

    def _action_return(self, note=False):
        for record in self:
            record.write({'state': 'draft'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_sale')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_sale')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            
            # add pending tickets for requester user_id
            user_ids = record.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_resubmit',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    #record.write({'ticket_ids': [(0, 0, datas)]})
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #record.offer_notes = str(datas)
                    #record.request_notes = str(new_ticket)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
            record.compute_items_stats()
    
    def action_wizard_submit_selection(self):

        return {
            'name': 'Submit Selection',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_submit_selection'
                }
        }

    def _action_submit_selection(self, note=False):
        for record in self:
            record.write({'state': 'confirmation'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action in ['req_cost_submit','req_cost_resubmit'])
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.id),('state','=','open'),('action','=','req_cost_select')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket(s) for each requested item's assigned user to request ticket_ids and item ticket_ids
            selected_items = record.request_item_ids.filtered(lambda r: r.state == 'selected')
            if selected_items:
                for item in selected_items:
                    item.state = 'to_confirm'
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'request_costing_item_id': item.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': item.assigned_user_id.id,
                        'action':'req_cost_confirm_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state':'open',
                    }
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #item.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #item.ticket_ids = [(4, new_ticket.id)]
                    #record.ticket_ids = [(4, new_ticket.id)]

            record.compute_items_stats()
            


    def action_wizard_cancel(self):

        return {
            'name': 'Cancel Request',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_cancel'
                }
        }

    def _action_cancel(self, note=False):
        for record in self:
            record.write({'state': 'cancel'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action in ['req_cost_submit','req_cost_resubmit'])
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.id),('state','=','open')])
            if related_ticket_ids:
                datas = {
                    'state':'cancel',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)
            record.so_line_id.request_costing_id = False
            record.compute_items_stats()
            
            
    


    def action_request_request_costing_wizard(self):
        result = {
            "name": "Request Costing Request Items",
            "type": "ir.actions.act_window",
            "res_model": "cmo.request.wizard",
            "view_mode": "form",
            "target":"new",
            "context": {
                "default_wizard_type": "update",
                "default_request_id": self.id,
                "default_assigned_user_id": self.assigned_user_id.id or self.product_id.procurement_user_id.id or False,
                },
        }
        return result

    def action_generate_po_mass(self):
        for record in self.request_item_ids.filtered(lambda r: r.type == 'external' and not r.po_id):
            record.generate_po()
        self.compute_items_stats()


    

    #permission and view fields
    can_edit_request = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_edit_offer = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_delete = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_cancel = fields.Boolean(compute="_compute_user_permissions", store=False)
        
    can_submit = fields.Boolean(compute="_compute_user_permissions", store=False)
    
    can_validate = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_return = fields.Boolean(compute="_compute_user_permissions", store=False)

    can_submit_selection = fields.Boolean(compute="_compute_user_permissions", store=False)

    can_add_item = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_request_item = fields.Boolean(compute="_compute_user_permissions", store=False)
    can_generate_po = fields.Boolean(compute="_compute_user_permissions", store=False)

    @api.depends('state','is_requester_any','is_assigned_any')
    def _compute_user_permissions(self):
        for record in self:
            record.can_edit_request = False
            record.can_edit_offer = False
            record.can_delete = False
            record.can_cancel = False
            record.can_submit = False
            record.can_validate = False
            record.can_return = False
            record.can_submit_selection = False
            record.can_request_item = False
            record.can_add_item = False
            record.can_generate_po = False

            if record.state in ['draft'] and record.is_requester_any:                
                record.can_edit_request = True

            if record.state in ['costing'] and record.is_assigned_any:                
                record.can_edit_offer = True

            if record.state not in ['cancel'] and record.is_requester_any:                
                record.can_cancel = True

            if record.state in ['draft','selection'] and record.is_requester_any and len(record.request_item_ids.filtered(lambda r: r.state == 'draft')) > 0:
                record.can_submit = True

            if record.state in ['sale_validation'] and (record.is_requester_manager or record.is_requester_ou_manager) :
                record.can_validate = True
                record.can_return = True
            
            if record.state in ['selection'] and record.is_requester_any and len(record.request_item_ids.filtered(lambda r: r.state == 'selected')) > 0 and len(record.request_item_ids.filtered(lambda r: r.state == 'draft')) == 0:
                record.can_submit_selection = True

            if (record.state in ['draft','selection'] and record.is_requester_any):
                record.can_request_item = True

            if (record.state == 'costing' and record.is_assigned_any):
                record.can_add_item = True
            
            if record.state in ['costing'] and record.is_assigned_any and len(record.request_item_ids.filtered(lambda r: not r.po_id)) > 0:                
                record.can_generate_po = True





class CostingRequestItem(models.Model):
    _name = "request.costing.item"
    _description = "Costing Request Item"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #User Data
    current_user_id = fields.Many2one('res.users', default=lambda self: self.env.user, store=False)
    
    current_operating_unit_ids = fields.One2many(comodel_name="operating.unit", string="Allowed Units", related="current_user_id.operating_unit_ids", store=False)
    current_operating_unit_sales_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Units", compute_sudo=True, store=False)
    current_operating_unit_sales_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Sales Ops Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Units", compute_sudo=True, store=False)
    current_operating_unit_procurement_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Procurement Ops Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Units", compute_sudo=True, store=False)
    current_operating_unit_finance_ops_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Finance Ops Units", compute_sudo=True, store=False)
    current_operating_unit_hr_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="HR Units", compute_sudo=True, store=False)
    current_operating_unit_it_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="IT Units", compute_sudo=True, store=False)
    current_operating_unit_marketing_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Marketing Units", compute_sudo=True, store=False)
    current_operating_unit_executive_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Executive Units", compute_sudo=True, store=False)
    current_operating_unit_virtual_ids = fields.One2many(comodel_name="operating.unit", compute="_compute_current_operating_unit_ids", string="Virtual Units", compute_sudo=True, store=False)

    current_operating_unit_sales_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_id", string="Sales Unit", store=False)
    current_operating_unit_sales_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_sales_ops_id", string="Sales Ops Unit", store=False)
    current_operating_unit_procurement_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_id", string="Procurement Unit", store=False)
    current_operating_unit_procurement_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_procurement_ops_id", string="Procurement Ops Unit", store=False)
    current_operating_unit_finance_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_id", string="Finance Unit", store=False)
    current_operating_unit_finance_ops_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_finance_ops_id", string="Finance Ops Unit", store=False)
    current_operating_unit_hr_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_hr_id", string="HR Unit", store=False)
    current_operating_unit_it_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_it_id", string="IT Unit", store=False)
    current_operating_unit_marketing_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_marketing_id", string="Marketing Unit", store=False)
    current_operating_unit_executive_id = fields.Many2one(comodel_name="operating.unit", related="current_user_id.default_operating_unit_executive_id", string="Executive Unit", store=False)

    @api.depends("current_user_id", "current_operating_unit_ids")
    def _compute_current_operating_unit_ids(self):
        for user in self:
            user.current_operating_unit_sales_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales')
            user.current_operating_unit_sales_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'sales_ops')
            user.current_operating_unit_procurement_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement')
            user.current_operating_unit_procurement_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'procurement_ops')
            user.current_operating_unit_finance_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance')
            user.current_operating_unit_finance_ops_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'finance_ops')
            user.current_operating_unit_hr_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'hr')
            user.current_operating_unit_it_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'it')
            user.current_operating_unit_executive_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'executive')
            user.current_operating_unit_virtual_ids = user.current_operating_unit_ids.filtered(lambda r: r.function == 'virtual')
    


    is_requester_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_ou_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_ou_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_ou_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_ou_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_user(self):
        for record in self:
            record.is_requester_user = record.current_user_id == record.requester_user_id
            record.is_requester_ou_user = record.current_user_id in record.requester_ou_id.user_ids and (record.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or record.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))
            record.is_requester_ou_manager = record.current_user_id == record.requester_ou_id.manager_id
            record.is_requester_manager = record.env.user.has_group('sales_team.group_sale_manager')
            record.is_requester_any = record.is_requester_user or record.is_requester_ou_user or record.is_requester_ou_manager or record.is_requester_manager
            
            record.is_assigned_user = record.current_user_id == record.assigned_user_id
            record.is_assigned_ou_user = record.current_user_id in record.assigned_ou_id.user_ids and (record.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or record.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))
            record.is_assigned_ou_manager = record.current_user_id == record.assigned_ou_id.manager_id
            record.is_assigned_manager = record.env.user.has_group('purchase.group_purchase_manager')
            record.is_assigned_any = record.is_assigned_user or record.is_assigned_ou_user or record.is_assigned_ou_manager or record.is_assigned_manager


    """
    is_sale_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_leader = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_requester_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_team_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_ou_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_assigned_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_pa_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_user(self):
        for record in self:

            
            record.is_sale_user = False
            record.is_sale_team_user = False
            record.is_sale_team_leader = False
            record.is_sale_manager = False
            record.is_requester_any = False

            record.is_purchase_user = False
            record.is_purchase_team_user = False
            record.is_assigned_ou_manager = False
            record.is_assigned_manager = False
            record.is_assigned_any = False

            

            if record.current_user_id and record.request_id:
                if record.request_id.requester_user_id:
                    record.is_sale_user = record.current_user_id == record.request_id.requester_user_id
            
            if record.current_user_id and record.current_operating_unit_sales_id and record.request_id:
                if record.request_id.sales_ou_id:
                    record.is_sale_team_user = record.current_operating_unit_sales_id == record.request_id.sales_ou_id and (self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))

            if record.current_user_id and record.current_operating_unit_sales_id and record.request_id:
                if record.request_id.sales_ou_id:
                    if record.request_id.sales_ou_id.manager_id:
                        record.is_sale_team_leader = record.current_user_id == record.request_id.sales_ou_id.manager_id

            record.is_sale_manager = self.env.user.has_group('sales_team.group_sale_manager')
            record.is_requester_any = record.is_sale_user or record.is_sale_team_user or record.is_sale_team_leader or record.is_sale_manager

            if record.current_user_id and record.assigned_user_id:
                record.is_purchase_user = record.current_user_id == record.assigned_user_id

            if record.current_user_id and record.current_operating_unit_procurement_id and record.request_id:
                if record.request_id.assigned_ou_id:
                    record.is_sale_team_user = record.current_operating_unit_sales_id == record.request_id.sales_ou_id and (self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))


            self.is_purchase_team_user = self.current_operating_unit_procurement_id == self.assigned_ou_id and (self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_all_docs') or self.env.user.has_group('ges_logistics_request_costing.group_request_costing_user_team_docs'))


            if record.current_user_id and record.assigned_user_id:
                if record.assigned_ou_id.manager_id:
                    record.is_assigned_ou_manager = record.current_user_id == record.assigned_ou_id.manager_id 
            
            record.is_assigned_manager = self.env.user.has_group('purchase.group_purchase_manager')
            record.is_assigned_any = record.is_purchase_user or record.is_assigned_ou_manager or record.is_assigned_manager
        
    """

    #generic fields
    active = fields.Boolean(default=True, string='Active')
    requester_user_id = fields.Many2one('res.users', string='Request User', index=True, default=lambda self: self.env.user)
    
    requester_ou_id = fields.Many2one(
        comodel_name='operating.unit',
        string="Request Unit",
        related='requester_user_id.default_operating_unit_sales_id',
        store=True)   

    color = fields.Integer('Color')
    sequence = fields.Integer(string="Sequence")
    
    #Parent Fields
    request_id = fields.Many2one('request.costing', string="Request")
    request_state = fields.Selection(related="request_id.state")
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict', related="request_id.partner_id")
    company_id = fields.Many2one(related='request_id.company_id', store=True, index=True, precompute=True)
    sol_currency_id = fields.Many2one(related='request_id.so_line_id.currency_id', depends=['request_id.so_line_id.currency_id'], store=True, precompute=True)

    #user Fields
    assigned_user_id = fields.Many2one(comodel_name='res.users', string="Assigned User", compute='_compute_assigned_user_id', store=True, readonly=False, index=True)
    assigned_ou_id = fields.Many2one(comodel_name='operating.unit', string="Assigned Unit", related='assigned_user_id.default_operating_unit_procurement_id', store=True) 

    #tickets fields
    ticket_ids = fields.One2many('ticket','request_costing_item_id', string="Tickets")

    @api.depends('vendor_id','product_id','type')
    @api.onchange('vendor_id','product_id','type')
    def _compute_assigned_user_id(self):
        for record in self:
            if record.type == 'external':
                if record.vendor_id and not (record._origin.id and record.assigned_user_id):
                    if record.vendor_id.procurement_user_id:
                        record.assigned_user_id = record.vendor_id.procurement_user_id
                    elif record.vendor_id.country_id.procurement_user_id:
                        record.assigned_user_id = record.vendor_id.country_id.procurement_user_id
                    else:
                        record.assigned_user_id = False
            elif record.type == 'internal':
                if record.product_id and not (record._origin.id and record.assigned_user_id):
                    if record.product_id.procurement_user_id:
                        record.assigned_user_id = record.product_id.procurement_user_id
                    elif record.product_id.categ_id.procurement_user_id:
                        record.assigned_user_id = record.product_id.categ_id.procurement_user_id
                    else:
                        record.assigned_user_id = False

    #item fields
    name = fields.Char(string="Name")
    type = fields.Selection([('internal','Internal'),('external','External')], string="Type")
    note = fields.Html("Notes")

    #state fields

    previous_state = fields.Char()

    state_item_selections = [
        ('draft', 'Draft'),
        ('to_quote', 'To Quote'),
        ('to_validate','To Validate'),
        ('to_validate_failed','To Validate'),
        ('quoted', 'Quoted'),
        ('suggested', 'Suggested'),
        ('failed', 'Failed'), 
        ('required', 'Required'),
        ('selected','Selected'),
        ('to_confirm','To Confirm'),
        ('confirmed','Confirmed'),
        ('rejected_selection', 'Rejected'), 
        ('to_bill', 'To Bill'),
        ('billed', 'Billed'),
        ('rejected_billing', 'Rejected'),
        ('cancel', 'Cancelled'),
    ]
    state = fields.Selection(selection=state_item_selections, default='draft', string='Status')

    requested = fields.Boolean("Requested", default=False)
    to_send = fields.Boolean("To Send", compute="_compute_to_send", store=True)
    waiting = fields.Boolean("Waiting", compute="_compute_waiting", store=True)
    late = fields.Boolean("Late", compute="_compute_late", store=True)
    
    """
    to_validate = fields.Boolean("To Validate", default=False)
    to_validate_failed = fields.Boolean("To Validate", default=False)
    quoted = fields.Boolean("Quoted", default=False)
    failed = fields.Boolean("Failed", default=False)
    suggested = fields.Selection([('0', 'Normal'), ('1', 'Suggested')], 'Suggestion', default='0', index=True)
    required = fields.Boolean("Required", default=False)
    selected = fields.Boolean("Selected", default=False, compute='_compute_selected', store=True, readonly=False)
    to_confirm = fields.Boolean("To Confirm", default=False)
    confirmed = fields.Boolean("Confirmed", default=False)
    rejected_selection = fields.Boolean("Rejected Selection", default=False)
    to_bill = fields.Boolean("To Bill", default=False)
    billed = fields.Boolean("Billed", default=False)
    rejected_billing = fields.Boolean("Rejected Billing", default=False)
    cancelled = fields.Boolean("Cancelled", default=False)
    """

    @api.depends('type','po_id','po_id.state','state')
    def _compute_to_send(self):
        for record in self:
            record.to_send = False
            if record.type == 'external' and record.po_id and record.state == 'to_quote':
                record.to_send = True if record.po_id.state == 'draft' else False

    @api.depends('type','po_id','po_id.state','po_id.date_order','state')
    def _compute_waiting(self):
        for record in self:
            record.waiting = False
            if record.type == 'external' and record.po_id:
                condition = (record.po_id.state == 'sent') and (record.po_id.date_order >= fields.Datetime.now()) and record.state == 'to_quote'
                record.waiting = True if condition else False

    @api.depends('type','po_id', 'po_id.state','po_id.date_order','request_id','request_id.target_date','state')
    def _compute_late(self):
        for record in self:
            record.late = False
            if record.type == 'external':
                #condition = (record.po_id.state in ['draft','sent','to approve']) and (record.po_id.date_order < fields.Datetime.now())
                condition = record.request_id.target_date < fields.Datetime.now() if record.request_id.target_date else False and not record.state == 'cancel'
                record.late = True if condition else False
            elif record.type == 'internal':
                if record.request_id.target_date:
                    condition = record.request_id.target_date < fields.Datetime.now() if record.request_id.target_date else False and not record.state == 'cancel'
                    record.late = True if condition else False

    @api.depends('type')
    def _clear_other_fields(self):
        for record in self:
            if record.type == 'internal':
                record.update({
                    'vendor_id': False,
                    'po_id': False,
                })
            elif record.type == 'external':
                record.update({
                    'product_id': False,
                    'quantity': False,
                    'product_uom': False,
                    'price_unit': False,
                })


    #internal fields
    internal_vendor = fields.Many2one('res.partner', string='Internal Vendor', compute="_get_internal_vendor")
    product_id = fields.Many2one('product.product', string="Service/Product")
    product_currency_id = fields.Many2one(related='company_id.currency_id', depends=['company_id.currency_id'], store=True, precompute=True)
    quantity = fields.Integer("Quantity", default="1")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        compute='_compute_product_uom',
        store=True, readonly=False, precompute=True, ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]") 
    price_unit = fields.Float(
        string="Unit Price",
        compute='_compute_price_unit',
        digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)
    total = fields.Monetary(string="Total", compute='_compute_total', store=True, precompute=True, currency_field="product_currency_id")
        
    @api.depends('type')
    @api.onchange('type')
    def _get_internal_vendor(self):
        for record in self:
            if record.type == 'internal':
                record.internal_vendor = self.env.company.partner_id.id
            else:
                record.internal_vendor = False

    @api.depends('product_id','type')
    def _compute_product_uom(self):
        for record in self:
            record.product_uom = False
            if record.type == 'internal':
                if not record.product_uom or (record.product_id.uom_id.id != record.product_uom.id):
                    record.product_uom = record.product_id.uom_id

    @api.depends('product_id','type')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = 0.0
            if record.type == 'internal' and record.product_id:
                record.price_unit = record.product_id.list_price

    @api.depends('type', 'quantity', 'price_unit', 'product_id','product_uom')
    def _compute_total(self):
        for record in self:
            record.update({'total': 0.0,})
            if record.type == 'internal':
                if record.quantity and record.product_id and record.price_unit:
                    product_uom = record.product_id.uom_id
                    target_uom = record.product_uom
                    if target_uom != product_uom:
                        qty_in_product_uom = target_uom._compute_quantity(record.quantity,product_uom,raise_if_failure=False)
                    else:
                        qty_in_product_uom = record.quantity
                    record.update({'total': record.price_unit * qty_in_product_uom,})

    #external fields
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    po_id = fields.Many2one('purchase.order', string="PO")
    po_vendor_id = fields.Many2one('res.partner', string="Vendor", related="po_id.partner_id")
    po_currency_id = fields.Many2one(related='po_id.currency_id', depends=['po_id.currency_id'], store=True, precompute=True)
    po_state = fields.Selection(string="Status", related="po_id.state")
    po_date_order = fields.Datetime(related="po_id.date_order")
    po_amount_untaxed = fields.Monetary(string="Untaxed Amount", related="po_id.amount_untaxed", currency_field="po_currency_id")
    po_amount_tax = fields.Monetary(string="Taxes", related="po_id.amount_tax", currency_field="po_currency_id")
    po_amount_total = fields.Monetary(string="Total", related="po_id.amount_total", currency_field="po_currency_id")
    
    applicable_po_total = fields.Monetary(string="Applicable PO Total", compute="_compute_applicable_po_total", currency_field="po_currency_id")
    
    applicable_so_total = fields.Monetary(string="Applicable SO Total", compute="_compute_applicable_po_total", currency_field="sol_currency_id")
    applicable_so_taxed = fields.Monetary(string="Applicable SO Taxed", compute="_compute_applicable_po_total", currency_field="sol_currency_id")
    applicable_so_untaxed = fields.Monetary(string="Applicable SO Untaxed", compute="_compute_applicable_po_total", currency_field="sol_currency_id")
    
    applicable_co_total = fields.Monetary(string="Applicable Company Total", compute="_compute_applicable_po_total", currency_field="product_currency_id")
    applicable_co_taxed = fields.Monetary(string="Applicable Company Taxed", compute="_compute_applicable_po_total", currency_field="product_currency_id")
    applicable_co_untaxed = fields.Monetary(string="Applicable Company Untaxed", compute="_compute_applicable_po_total", currency_field="product_currency_id")
    

    @api.depends('type','po_id','po_amount_total', 'po_amount_untaxed','total')
    def _compute_applicable_po_total(self):
        for record in self:
            record.applicable_po_total = 0
            record.applicable_so_total = 0
            record.applicable_so_taxed = 0
            record.applicable_so_untaxed = 0
            record.applicable_co_total = 0
            record.applicable_co_taxed = 0
            record.applicable_co_untaxed = 0
            
            if record.type == 'external' and record.po_id:
                record.applicable_so_taxed = record.po_currency_id._convert(record.po_amount_total,record.sol_currency_id,date=record.po_date_order)
                record.applicable_so_untaxed = record.po_currency_id._convert(record.po_amount_untaxed,record.sol_currency_id,date=record.po_date_order)
                record.applicable_co_taxed = record.po_currency_id._convert(record.po_amount_total,record.product_currency_id,date=record.po_date_order)
                record.applicable_co_untaxed = record.po_currency_id._convert(record.po_amount_untaxed,record.product_currency_id,date=record.po_date_order)  
                if self.env.company.vat:
                    record.applicable_po_total = record.po_amount_untaxed
                    record.applicable_so_total = record.po_currency_id._convert(record.po_amount_untaxed,record.sol_currency_id,date=record.po_date_order)
                    record.applicable_co_total = record.po_currency_id._convert(record.po_amount_untaxed,record.product_currency_id,date=record.po_date_order)
                else:
                    record.applicable_po_total = record.po_amount_total
                    record.applicable_so_total = record.po_currency_id._convert(record.po_amount_total,record.sol_currency_id,date=record.po_date_order)
                    record.applicable_co_total = record.po_currency_id._convert(record.po_amount_total,record.product_currency_id,date=record.po_date_order)

            if record.type == 'internal':
                if record.sol_currency_id:
                    record.applicable_so_taxed = record.product_currency_id._convert(record.total,record.sol_currency_id,date=record.request_id.so_id.date_order)
                    record.applicable_so_untaxed = record.product_currency_id._convert(record.total,record.sol_currency_id,date=record.request_id.so_id.date_order)
                    record.applicable_so_total = record.product_currency_id._convert(record.total,record.sol_currency_id,date=record.request_id.so_id.date_order)

                record.applicable_co_taxed = record.total
                record.applicable_co_untaxed = record.total
                record.applicable_co_total = record.total
            
            

    #Actions

    def open_po(self):
 
        result = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'purchase.order',
                'target': 'current',
                'res_id': self.po_id.id,
                'domain': [('id','=',self.po_id.id)],
            } 
        return result 

    def action_wizard_submit_quote(self):

        return {
            'name': 'Submit Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_submit_quote'
                }
        }

    def _submit_quote(self, note=False):
        for record in self:

            record.state = 'to_validate' 

            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_cost_item')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_cost_item')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)
            
            # add pending ticket(s) for assigned_ou_id team leaders

            user_ids = record.assigned_ou_id.manager_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_purchase',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #raise UserError(str(new_ticket.id))
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()


    def action_wizard_validate_quote(self):

        return {
            'name': 'Validate Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_validate_quote'
                }
        }

    def _validate_quote(self, note=False):
        for record in self:

            record.state = 'quoted' 
        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state in ['draft','to_quote'])
            if not pending_items:
                check_if_any_quoted = record.request_id.request_item_ids.filtered(lambda r: r.state == 'quoted')
                if not check_if_any_quoted:
                    record.request_id.state = 'unsuccessful'
                else:
                    record.request_id.state = 'selection'
                
                    # add pending ticket(s) to item and request for requester user_id

                    user_ids = record.request_id.requester_user_id.id
                    user_records = False
                    if user_ids:
                        user_records = self.env['res.users'].search([('id','=',user_ids)])
                    if user_records:
                        for user in user_records:
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].sudo().create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()


    def action_wizard_return_quote(self):

        return {
            'name': 'Return Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_return_quote'
                }
        }

    def _return_quote(self, note=False):
        for record in self:

            record.state = 'to_quote'
        
            #close current related tickets and add note
            
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket to item and request for item assigned_user_id

            user_ids = record.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()

    def action_wizard_submit_failed(self):

        return {
            'name': 'Failed to Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_submit_failed'
                }
        }

    def _submit_failed(self, note=False):
        for record in self:

            record.state = 'to_validate_failed'
            

            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_cost_item')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_cost_item')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)
            
            # add pending ticket(s) for assigned_ou_id team leaders

            user_ids = record.assigned_ou_id.manager_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_purchase',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    new_ticket = self.env['ticket'].sudo().create(datas)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()

    def action_wizard_validate_failed(self):

        return {
            'name': 'Validate Failed Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_validate_failed'
                }
        }

    def _validate_failed(self, note=False):
        for record in self:

            record.state = 'failed'
        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state not in ['quoted','failed'])
            if not pending_items:

                check_if_any_quoted = record.request_id.request_item_ids.filtered(lambda r: r.state == 'quoted')
                if not check_if_any_quoted:
                    record.request_id.state = 'unsuccessful'
                else:
                    record.request_id.state = 'selection'
                
                    # add pending ticket(s) to item and request for requester user_id

                    user_ids = record.request_id.requester_user_id.id
                    user_records = False
                    if user_ids:
                        user_records = self.env['res.users'].search([('id','=',user_ids)])
                    if user_records:
                        for user in user_records:
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            new_ticket = self.env['ticket'].sudo().create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()


    def action_wizard_return_failed(self):

        return {
            'name': 'Return Failed Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_return_failed'
                }
        }

    def _return_failed(self, note=False):
        for record in self:

            record.state = 'to_quote'
        
            #close current related tickets and add note
            
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket to item and request for item assigned_user_id

            user_ids = record.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'requester_user_id': self.env.user.id,
                        'requester_note': note,
                        'user_id': user.id,                        
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].sudo().create(datas)

            record.request_id.compute_items_stats()


    def mark_selected(self):
        for record in self:
            record.previous_state = record.state
            record.state = 'selected'

    def remove_mark_selected(self):
        for record in self:
            record.state = record.previous_state


    def action_wizard_recost(self):

        return {
            'name': 'Request Recosting',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_recost'
                }
        }

    def _recost(self, note=False):
        for record in self:

            record.state = 'to_quote'
            record.request_id.state = 'costing'
            
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_id','=',record.request_id.id),('state','=','open'),('action','=','req_cost_select')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            datas = {
                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                'request_costing_id': record.request_id.id,
                'request_costing_item_id': record.id,
                'requester_user_id': self.env.user.id,
                'requester_note': note,
                'user_id': record.assigned_user_id.id,                        
                'action':'req_cost_cost_item',
                'opened_datetime': fields.Datetime.now(),
                'state': 'open',
            }
            
            new_ticket = self.env['ticket'].sudo().create(datas)
             
            record.request_id.compute_items_stats()



    def action_wizard_confirm_quote(self):

        return {
            'name': 'Confirm Selection',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_confirm_quote'
                }
        }

    def _confirm_quote(self, note=False):
        for record in self:

            record.state = 'confirmed'
        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_confirm_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'to_confirm')
            if not pending_items:
                check_if_any_rejected = record.request_id.request_item_ids.filtered(lambda r: r.state == 'rejected_selection')
                if not check_if_any_rejected:
                    record.request_id.state = 'billing'
                    confirmed_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'confirmed')
                    if confirmed_items:
                        for item in confirmed_items:
                            item.state = 'to_bill'
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': item.assigned_user_id.id,                        
                                'action':'req_cost_bill_item',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].sudo().create(datas)
                else:
                    record.request_id.state = 'selection'
                
                    # add pending ticket(s) to item and request for requester user_id

                    user_ids = record.request_id.requester_user_id.id
                    user_records = False
                    if user_ids:
                        user_records = self.env['res.users'].search([('id','=',user_ids)])
                    if user_records:
                        for user in user_records:
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].sudo().create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()

    def action_wizard_reject_quote(self):

        return {
            'name': 'Reject Selection',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_reject_quote'
                }
        }

    def _reject_quote(self, note=False):
        for record in self:

            record.state = 'rejected_selection'
        
            #close current related tickets and add note
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_confirm_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'to_confirm')
            if not pending_items:
                check_if_any_rejected = record.request_id.request_item_ids.filtered(lambda r: r.state == 'rejected_selection')
                if not check_if_any_rejected:
                    record.request_id.state = 'billing'
                    confirmed_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'confirmed')
                    if confirmed_items:
                        for item in confirmed_items:
                            item.state = 'to_bill'
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': item.assigned_user_id.id,                        
                                'action':'req_cost_bill_item',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].sudo().create(datas)
                else:
                    record.request_id.state = 'selection'
                
                    # add pending ticket(s) to item and request for requester user_id

                    user_ids = record.request_id.requester_user_id.id
                    user_records = False
                    if user_ids:
                        user_records = self.env['res.users'].search([('id','=',user_ids)])
                    if user_records:
                        for user in user_records:
                            datas = {
                                'reference_document': ('%s,%s' % ('request.costing', record.request_id.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'requester_user_id': self.env.user.id,
                                'requester_note': note,
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].sudo().create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
            record.request_id.compute_items_stats()

    def remove_rejected_selection(self):
        for record in self:
            record.state = record.previous_state

    def action_wizard_bill_quote(self):

        return {
            'name': 'Bill Quote',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_bill_quote'
                }
        }

    def _bill_quote(self, note=False):
        for record in self:

            record.state = 'billed'
        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_bill_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'to_bill')
            if not pending_items:
                check_if_any_rejected = record.request_id.request_item_ids.filtered(lambda r: r.state == 'rejected_billing')
                if not check_if_any_rejected:
                    record.request_id.state = 'done'
                else:
                    record.request_id.state = 'confirmation'
                
                    for item in check_if_any_rejected:
                        datas = {
                            'reference_document': ('%s,%s' % ('request.costing', record.id)),
                            'request_costing_id': record.request_id.id,
                            'request_costing_item_id': record.id,
                            'requester_user_id': self.env.user.id,
                            'requester_note': note,
                            'user_id': item.assigned_user_id.id,
                            'action':'req_cost_confirm_item',
                            'opened_datetime': fields.Datetime.now(),
                            'state':'open',
                        }
                        new_ticket = self.env['ticket'].sudo().create(datas)
                        #item.write({'ticket_ids': [(4, new_ticket.id)]})
                        #record.write({'ticket_ids': [(4, new_ticket.id)]})
                        #item.ticket_ids = [(4, new_ticket.id)]
                        #record.ticket_ids = [(4, new_ticket.id)]
            record.request_id.compute_items_stats()

    def action_wizard_reject_bill(self):

        return {
            'name': 'Reject Billing',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_reject_bill'
                }
        }

    def _reject_bill(self, note=False):
        for record in self:

            record.state = 'rejected_billing'
        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open'),('action','=','req_cost_bill_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state == 'to_bill')
            if not pending_items:
                check_if_any_rejected = record.request_id.request_item_ids.filtered(lambda r: r.state == 'rejected_billing')
                if not check_if_any_rejected:
                    record.request_id.state = 'done'
                else:
                    record.request_id.state = 'confirmation'
                
                    for item in check_if_any_rejected:
                        datas = {
                            'reference_document': ('%s,%s' % ('request.costing', record.id)),
                            'request_costing_id': record.request_id.id,
                            'request_costing_item_id': record.id,
                            'requester_user_id': self.env.user.id,
                            'requester_note': note,
                            'user_id': item.assigned_user_id.id,
                            'action':'req_cost_confirm_item',
                            'opened_datetime': fields.Datetime.now(),
                            'state':'open',
                        }
                        new_ticket = self.env['ticket'].sudo().create(datas)
                        #item.write({'ticket_ids': [(4, new_ticket.id)]})
                        #record.write({'ticket_ids': [(4, new_ticket.id)]})
                        #item.ticket_ids = [(4, new_ticket.id)]
                        #record.ticket_ids = [(4, new_ticket.id)]
            record.request_id.compute_items_stats()



    def action_wizard_cancel_item(self):

        return {
            'name': 'Cancel Item',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_item_ids': self.ids,
                'default_name': 'req_cost_item_cancel'
                }
        }

    def _cancel_item(self, note=False):
        for record in self:

            record.state == 'cancel'

        
            #close current related tickets and add note
            
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_purchase')
            related_ticket_ids = self.env['ticket'].sudo().search([('request_costing_item_id','=',record.id),('state','=','open')])
            
            if related_ticket_ids:
                datas = {
                    'state':'cancel',
                    'closed_datetime': fields.Datetime.now(),
                    'assignee_note': note,
                }
                related_ticket_ids.write(datas)

            record.request_id.compute_items_stats()

    def generate_po(self):
        for record in self:
            if not record.po_id:
                line_dict = {
                    'partner_id': record.vendor_id.id,
                    'currency_id': record.vendor_id.property_purchase_currency_id.id or record.product_currency_id.id,
                    'payment_term_id': record.vendor_id.property_supplier_payment_term_id.id,
                    'date_order': record.request_id.target_date or None,
                    'order_line': [(0,0,{
                        'product_id': record.request_id.so_line_id.product_id.id,
                        'reference_document': str('%s,%s' % (record.request_id.so_line_id.reference_document._name, record.request_id.so_line_id.reference_document.id)),
                        'product_uom': record.request_id.so_line_id.product_uom.id,
                        'product_qty': record.request_id.so_line_id.product_uom_qty,
                    })]
                }
                new_po = self.env['purchase.order'].create(line_dict)
                record.po_id = new_po.id

            record.request_id.compute_items_stats()
    
    def action_delete_item(self):
        for record in self:
            record.unlink()
    

    #permission and view fields
    can_create = fields.Boolean(compute="_compute_can_create", store=False)
    can_edit = fields.Boolean(compute="_compute_can_edit", store=False)
    can_delete = fields.Boolean(compute="_compute_can_delete", store=False)
    can_cancel = fields.Boolean(compute="_compute_can_cancel", store=False)
    
    can_generate_po = fields.Boolean(compute="_compute_can_generate_po", store=False)
    
    can_submitted = fields.Boolean(compute="_compute_can_submitted", store=False)
    can_validated = fields.Boolean(compute="_compute_can_validated", store=False)
    can_failed = fields.Boolean(compute="_compute_can_failed", store=False)
    can_validate_failed = fields.Boolean(compute="_compute_can_validate_failed", store=False)

    can_quoted = fields.Boolean(compute="_compute_can_quoted", store=False)
    
    can_suggested = fields.Boolean(compute="_compute_can_suggested", store=False)
    can_required = fields.Boolean(compute="_compute_can_required", store=False)
    can_selected = fields.Boolean(compute="_compute_can_selected", store=False)
    can_confirm_selection = fields.Boolean(compute="_compute_can_confirm_selection", store=False)
    can_reject_selection = fields.Boolean(compute="_compute_can_reject_selection", store=False)
    can_billed = fields.Boolean(compute="_compute_can_billed", store=False)

    can_remove_quoted = fields.Boolean(compute="_compute_can_remove_quoted", store=False)
    can_remove_failed = fields.Boolean(compute="_compute_can_remove_failed", store=False)
    can_remove_suggested = fields.Boolean(compute="_compute_can_remove_suggested", store=False)
    can_remove_required = fields.Boolean(compute="_compute_can_remove_required", store=False)
    can_remove_selected = fields.Boolean(compute="_compute_can_remove_selected", store=False)
    can_remove_confirmed = fields.Boolean(compute="_compute_can_remove_confirmed", store=False)
    can_remove_billed = fields.Boolean(compute="_compute_can_remove_billed", store=False)

    @api.depends('request_id.state','is_requester_any','is_assigned_any')
    def _compute_can_create(self):
        for record in self:
            record.can_create = False
            if (record.request_id.state == 'draft' and record.is_requester_any) or (record.request_id.state == 'selection' and record.is_assigned_any):
                record.can_create = True
    
    @api.depends('request_id.state','requested')
    def _compute_can_edit(self):
        for record in self:
            record.can_edit = False
            if (record.request_id.state in ['draft'] and record.is_requester_any and record.requested) or (record.request_id.state in ['costing'] and record.is_assigned_any):                
                record.can_edit = True
        
    @api.depends('request_id.state','requested')
    def _compute_can_delete(self):
        for record in self:
            record.can_delete = False
            if (record.request_id.state in ['draft'] and record.is_requester_any and record.requested) or (record.request_id.state in ['costing'] and record.is_assigned_any and not record.requested):                
                record.can_delete = True

    @api.depends('request_id.state','state')
    def _compute_can_cancel(self):
        for record in self:
            record.can_cancel = False
            if (record.request_id.state not in ['draft'] and record.is_requester_any and not record.state == 'cancel') or (record.request_id.state in ['costing'] and record.is_assigned_any and not record.state == 'cancel'):                
                record.can_cancel = True
    
    @api.depends('request_id.state','type','po_id')
    def _compute_can_generate_po(self):
        for record in self:
            record.can_generate_po = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.type == 'external' and not record.po_id:                
                record.can_generate_po = True

    @api.depends('request_id.state','po_id','type','state')
    def _compute_can_submitted(self):
        for record in self:
            record.can_submitted = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and ((record.type == 'external' and record.po_id) or (record.type == 'internal')) and record.state in ['draft','to_quote']:
                record.can_submitted = True

    @api.depends('request_id.state','po_id','state')
    def _compute_can_validated(self):
        for record in self:
            record.can_validated = False
            if record.request_id.state in ['costing'] and (record.is_assigned_ou_manager or record.is_assigned_manager) and record.state in ['to_validate']:
                record.can_validated = True

    @api.depends('request_id.state','state')
    def _compute_can_failed(self):
        for record in self:
            record.can_failed = False
            if record.can_quoted == True and record.request_id.state in ['costing'] and record.is_assigned_any and record.state in ['draft','to_quote']:
                record.can_failed = True

    @api.depends('request_id.state','po_id','state')
    def _compute_can_validate_failed(self):
        for record in self:
            record.can_validate_failed = False
            if record.request_id.state in ['costing'] and (record.is_assigned_ou_manager or record.is_assigned_manager) and record.state == 'to_validate_failed':
                record.can_validate_failed = True


    @api.depends('request_id.state','po_id','type','state')
    def _compute_can_quoted(self):
        for record in self:
            record.can_quoted = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and ((record.type == 'external' and record.po_id) or (record.type == 'internal')) and record.state not in ['quoted','failed','to_validate','to_validate_failed']:
                record.can_quoted = True
    
    @api.depends('request_id.state','state')
    def _compute_can_remove_quoted(self):
        for record in self:
            record.can_remove_quoted = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'quoted':
                record.can_remove_quoted = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_failed(self):
        for record in self:
            record.can_remove_failed = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'failed':
                record.can_remove_failed = True
    
    @api.depends('request_id.state','state')
    def _compute_can_suggested(self):
        for record in self:
            record.can_suggested = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'quoted':
                record.can_suggested = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_suggested(self):
        for record in self:
            record.can_remove_suggested = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'suggested':
                record.can_remove_suggested = True
    
    @api.depends('request_id.state','state')
    def _compute_can_required(self):
        for record in self:
            record.can_required = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'quoted':
                record.can_required = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_required(self):
        for record in self:
            record.can_remove_required = False
            if record.request_id.state in ['costing'] and record.is_assigned_any and record.state == 'required':
                record.can_remove_required = True

    @api.depends('request_id.state','state','request_id.is_requester_any')
    def _compute_can_selected(self):
        for record in self:
            record.can_selected = False
            if record.request_id.state in ['selection','costing'] and record.request_id.is_requester_any and record.state in ['quoted','suggested']:
                record.can_selected = True

    @api.depends('request_id.state','state','request_id.is_requester_any')
    def _compute_can_remove_selected(self):
        for record in self:
            record.can_remove_selected = False
            if record.request_id.state in ['selection'] and record.request_id.is_requester_any and record.state == 'selected':
                record.can_remove_selected = True

    @api.depends('request_id.state','type','po_id.state','state')
    def _compute_can_confirm_selection(self):
        for record in self:
            record.can_confirm_selection = False
            if record.request_id.state in ['confirmation'] and record.is_assigned_any and ((record.type == 'external' and record.po_id and record.po_id.state in ['purchase','done']) or (record.type == 'internal')) and record.state == 'to_confirm':
                record.can_confirm_selection = True
    
    @api.depends('request_id.state','type','po_id.state','state')
    def _compute_can_reject_selection(self):
        for record in self:
            record.can_reject_selection = False
            if record.request_id.state in ['confirmation'] and record.is_assigned_any and record.state == 'confirmed':
                record.can_reject_selection = True

    @api.depends('request_id.state','type','po_id.state','state')
    def _compute_can_remove_confirmed(self):
        for record in self:
            record.can_remove_confirmed = False
            if record.request_id.state in ['confirmation'] and record.is_assigned_any and ((record.type == 'external' and record.po_id and record.po_id.state not in ['purchase','done']) or (record.type == 'internal')) and record.state == 'to_bill':
                record.can_remove_confirmed = True

    @api.depends('request_id.state','type','po_id.state','po_id.invoice_status','state')
    def _compute_can_billed(self):
        for record in self:
            record.can_billed = False
            if record.request_id.state in ['billing'] and record.is_assigned_any and ((record.type == 'external' and record.po_id and record.po_id.invoice_status == 'invoiced') or (record.type == 'internal')) and record.state == 'to_bill':
                record.can_billed = True

    @api.depends('request_id.state','po_id.state','po_id.invoice_status','state')
    def _compute_can_remove_billed(self):
        for record in self:
            record.can_remove_billed = False
            if record.request_id.state in ['billing'] and record.is_assigned_any and ((record.type == 'external' and record.po_id and record.po_id.invoice_status != 'invoiced') or (record.type == 'internal')) and record.state == 'billed':
                record.can_remove_billed = True
    