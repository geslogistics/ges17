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
            
    is_sale_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_leader = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_team_leader = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_pa_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_ou_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_user(self):
        self.is_pa_user = self.env.user.has_group('ges_logistics_application_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_own_docs')
        self.is_sale_user = self.current_user_id == self.requester_user_id
        self.is_sale_team_user = self.current_operating_unit_sales_id == self.sales_ou_id and (self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_team_docs'))
        self.is_sale_team_leader = self.current_user_id == self.sales_ou_id.manager_id
        self.is_sale_manager = self.env.user.has_group('sales_team.group_sale_manager')
        self.is_sale_any = self.is_sale_user or self.is_sale_team_user or self.is_sale_team_leader or self.is_sale_manager
        self.is_purchase_user = self.current_user_id in self.assigned_user_ids
        self.is_purchase_team_leader = self.current_user_id.id in self.assigned_ou_id.manager_id.ids
        self.is_purchase_manager = self.env.user.has_group('purchase.group_purchase_manager')
        self.is_purchase_any = self.is_purchase_user or self.is_purchase_team_leader or self.is_purchase_manager
        self.is_sale_ou_user = self.sales_ou_id in self.current_operating_unit_sales_ids and (self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_team_docs'))
        
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
            record.assigned_ou_id = record.request_item_ids.assigned_user_id.default_operating_unit_procurement_id.ids or False

            if record.assigned_user_id:
                record.assigned_user_ids = (([record.assigned_user_id.id] or None) + record.request_item_ids.assigned_user_id.ids) or False
            if record.assigned_ou_id:
                record.assigned_ou_id = (([record.assigned_ou_id.id] or None) + record.request_item_ids.assigned_user_id.default_operating_unit_procurement_id.ids) or False
                

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
    
    ### Stat Fields

    ## ALL ITEMS

    # ALL External Items Stats

    items_ex_requested = fields.Many2many('request.costing.item','exitems_requested', string="Requested", compute="_compute_items_stats")
    items_ex_to_send = fields.Many2many('request.costing.item','exitems_to_send', string="To Send", compute="_compute_items_stats")
    items_ex_waiting = fields.Many2many('request.costing.item','exitems_waiting', string="Waiting", compute="_compute_items_stats")
    items_ex_late = fields.Many2many('request.costing.item','exitems_late', string="Late", compute="_compute_items_stats")
    items_ex_to_quote = fields.Many2many('request.costing.item','exitems_to_quote', string="To Quote", compute="_compute_items_stats")
    items_ex_quoted = fields.Many2many('request.costing.item','exitems_quoted', string="Quoted", compute="_compute_items_stats")
    items_ex_quoted_high = fields.Many2many('request.costing.item','exitems_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_ex_quoted_low = fields.Many2many('request.costing.item','exitems_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_ex_suggested = fields.Many2many('request.costing.item','exitems_suggested', string="Suggested", compute="_compute_items_stats")
    items_ex_failed = fields.Many2many('request.costing.item','exitems_failed', string="Failed", compute="_compute_items_stats")
    items_ex_required = fields.Many2many('request.costing.item','exitems_required', string="Required", compute="_compute_items_stats")
    items_ex_selected = fields.Many2many('request.costing.item','exitems_selected', string="Selected", compute="_compute_items_stats")
    items_ex_to_confirm = fields.Many2many('request.costing.item','exitems_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_ex_confirmed = fields.Many2many('request.costing.item','exitems_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_ex_to_bill = fields.Many2many('request.costing.item','exitems_to_bill', string="To Bill", compute="_compute_items_stats")
    items_ex_billed = fields.Many2many('request.costing.item','exitems_billed', string="Billed", compute="_compute_items_stats")

    items_ex_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_ex_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_ex_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_ex_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_ex_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_ex_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_ex_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_ex_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_ex_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_ex_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_ex_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_ex_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_ex_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_ex_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_ex_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_ex_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_ex_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_ex_requested_vendors = fields.Many2many('res.partner','exitems_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_ex_to_send_vendors = fields.Many2many('res.partner','exitems_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_ex_waiting_vendors = fields.Many2many('res.partner','exitems_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_ex_late_vendors = fields.Many2many('res.partner','exitems_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_ex_to_quote_vendors = fields.Many2many('res.partner','exitems_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_ex_quoted_vendors = fields.Many2many('res.partner','exitems_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_ex_quoted_high_vendors = fields.Many2many('res.partner','exitems_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_ex_quoted_low_vendors = fields.Many2many('res.partner','exitems_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_ex_suggested_vendors = fields.Many2many('res.partner','exitems_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_ex_failed_vendors = fields.Many2many('res.partner','exitems_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_ex_required_vendors = fields.Many2many('res.partner','exitems_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_ex_selected_vendors = fields.Many2many('res.partner','exitems_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_ex_to_confirm_vendors = fields.Many2many('res.partner','exitems_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_ex_confirmed_vendors = fields.Many2many('res.partner','exitems_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_ex_to_bill_vendors = fields.Many2many('res.partner','exitems_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_ex_billed_vendors = fields.Many2many('res.partner','exitems_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_ex_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_ex_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_ex_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_ex_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_ex_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_ex_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_ex_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_ex_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_ex_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_ex_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_ex_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_ex_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_ex_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_ex_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_ex_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_ex_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_ex_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_ex_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_ex_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_ex_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_ex_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_ex_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    # ALL Internal Items Stats

    items_in_requested = fields.Many2many('request.costing.item','initems_requested', string="Requested", compute="_compute_items_stats")
    items_in_to_send = fields.Many2many('request.costing.item','initems_to_send', string="To Send", compute="_compute_items_stats")
    items_in_waiting = fields.Many2many('request.costing.item','initems_waiting', string="Waiting", compute="_compute_items_stats")
    items_in_late = fields.Many2many('request.costing.item','initems_late', string="Late", compute="_compute_items_stats")
    items_in_to_quote = fields.Many2many('request.costing.item','initems_to_quote', string="To Quote", compute="_compute_items_stats")
    items_in_quoted = fields.Many2many('request.costing.item','initems_quoted', string="Quoted", compute="_compute_items_stats")
    items_in_quoted_high = fields.Many2many('request.costing.item','initems_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_in_quoted_low = fields.Many2many('request.costing.item','initems_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_in_suggested = fields.Many2many('request.costing.item','initems_suggested', string="Suggested", compute="_compute_items_stats")
    items_in_failed = fields.Many2many('request.costing.item','initems_failed', string="Failed", compute="_compute_items_stats")
    items_in_required = fields.Many2many('request.costing.item','initems_required', string="Required", compute="_compute_items_stats")
    items_in_selected = fields.Many2many('request.costing.item','initems_selected', string="Selected", compute="_compute_items_stats")
    items_in_to_confirm = fields.Many2many('request.costing.item','initems_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_in_confirmed = fields.Many2many('request.costing.item','initems_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_in_to_bill = fields.Many2many('request.costing.item','initems_to_bill', string="To Bill", compute="_compute_items_stats")
    items_in_billed = fields.Many2many('request.costing.item','initems_billed', string="Billed", compute="_compute_items_stats")

    items_product_in_requested = fields.Many2many('product.product','initems_product_requested', string="Requested", compute="_compute_items_stats")
    items_product_in_quoted = fields.Many2many('product.product','initems_product_quoted', string="Quoted", compute="_compute_items_stats")
    items_product_in_suggested = fields.Many2many('product.product','initems_product_suggested', string="Suggested", compute="_compute_items_stats")
    items_product_in_failed = fields.Many2many('product.product','initems_product_failed', string="Failed", compute="_compute_items_stats")
    items_product_in_required = fields.Many2many('product.product','initems_product_required', string="Required", compute="_compute_items_stats")
    items_product_in_selected = fields.Many2many('product.product','initems_product_selected', string="Selected", compute="_compute_items_stats")
    items_product_in_confirmed = fields.Many2many('product.product','initems_product_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_product_in_billed = fields.Many2many('product.product','initems_product_billed', string="Billed", compute="_compute_items_stats")

    items_in_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_in_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_in_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_in_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_in_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_in_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_in_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_in_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_in_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_in_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_in_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_in_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_in_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_in_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_in_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_in_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_in_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_in_requested_vendors = fields.Many2many('res.partner','initems_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_in_to_send_vendors = fields.Many2many('res.partner','initems_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_in_waiting_vendors = fields.Many2many('res.partner','initems_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_in_late_vendors = fields.Many2many('res.partner','initems_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_in_to_quote_vendors = fields.Many2many('res.partner','initems_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_in_quoted_vendors = fields.Many2many('res.partner','initems_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_in_quoted_high_vendors = fields.Many2many('res.partner','initems_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_in_quoted_low_vendors = fields.Many2many('res.partner','initems_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_in_suggested_vendors = fields.Many2many('res.partner','initems_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_in_failed_vendors = fields.Many2many('res.partner','initems_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_in_required_vendors = fields.Many2many('res.partner','initems_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_in_selected_vendors = fields.Many2many('res.partner','initems_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_in_to_confirm_vendors = fields.Many2many('res.partner','initems_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_in_confirmed_vendors = fields.Many2many('res.partner','initems_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_in_to_bill_vendors = fields.Many2many('res.partner','initems_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_in_billed_vendors = fields.Many2many('res.partner','initems_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_in_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_in_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_in_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_in_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_in_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_in_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_in_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_in_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_in_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_in_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_in_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_in_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_in_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_in_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_in_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_in_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_in_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_in_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_in_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_in_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_in_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_in_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    # ALL Total Items Stats

    items_requested = fields.Many2many('request.costing.item','items_requested', string="Requested", compute="_compute_items_stats")
    items_to_send = fields.Many2many('request.costing.item','items_to_send', string="To Send", compute="_compute_items_stats")
    items_waiting = fields.Many2many('request.costing.item','items_waiting', string="Waiting", compute="_compute_items_stats")
    items_late = fields.Many2many('request.costing.item','items_late', string="Late", compute="_compute_items_stats")
    items_to_quote = fields.Many2many('request.costing.item','items_to_quote', string="To Quote", compute="_compute_items_stats")
    items_quoted = fields.Many2many('request.costing.item','items_quoted', string="Quoted", compute="_compute_items_stats")
    items_quoted_high = fields.Many2many('request.costing.item','items_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_quoted_low = fields.Many2many('request.costing.item','items_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_suggested = fields.Many2many('request.costing.item','items_suggested', string="Suggested", compute="_compute_items_stats")
    items_failed = fields.Many2many('request.costing.item','items_failed', string="Failed", compute="_compute_items_stats")
    items_required = fields.Many2many('request.costing.item','items_required', string="Required", compute="_compute_items_stats")
    items_selected = fields.Many2many('request.costing.item','items_selected', string="Selected", compute="_compute_items_stats")
    items_to_confirm = fields.Many2many('request.costing.item','items_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_confirmed = fields.Many2many('request.costing.item','items_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_to_bill = fields.Many2many('request.costing.item','items_to_bill', string="To Bill", compute="_compute_items_stats")
    items_billed = fields.Many2many('request.costing.item','items_billed', string="Billed", compute="_compute_items_stats")

    items_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_requested_vendors = fields.Many2many('res.partner','items_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_to_send_vendors = fields.Many2many('res.partner','items_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_waiting_vendors = fields.Many2many('res.partner','items_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_late_vendors = fields.Many2many('res.partner','items_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_to_quote_vendors = fields.Many2many('res.partner','items_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_quoted_vendors = fields.Many2many('res.partner','items_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_quoted_high_vendors = fields.Many2many('res.partner','items_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_quoted_low_vendors = fields.Many2many('res.partner','items_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_suggested_vendors = fields.Many2many('res.partner','items_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_failed_vendors = fields.Many2many('res.partner','items_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_required_vendors = fields.Many2many('res.partner','items_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_selected_vendors = fields.Many2many('res.partner','items_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_to_confirm_vendors = fields.Many2many('res.partner','items_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_confirmed_vendors = fields.Many2many('res.partner','items_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_to_bill_vendors = fields.Many2many('res.partner','items_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_billed_vendors = fields.Many2many('res.partner','items_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    ## REQUESTED ITEMS

    # REQUESTED External Items Stats

    items_exr_requested = fields.Many2many('request.costing.item','exitems_r_requested', string="Requested", compute="_compute_items_stats")
    items_exr_to_send = fields.Many2many('request.costing.item','exitems_r_to_send', string="To Send", compute="_compute_items_stats")
    items_exr_waiting = fields.Many2many('request.costing.item','exitems_r_waiting', string="Waiting", compute="_compute_items_stats")
    items_exr_late = fields.Many2many('request.costing.item','exitems_r_late', string="Late", compute="_compute_items_stats")
    items_exr_to_quote = fields.Many2many('request.costing.item','exitems_r_to_quote', string="To Quote", compute="_compute_items_stats")
    items_exr_quoted = fields.Many2many('request.costing.item','exitems_r_quoted', string="Quoted", compute="_compute_items_stats")
    items_exr_quoted_high = fields.Many2many('request.costing.item','exitems_r_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_exr_quoted_low = fields.Many2many('request.costing.item','exitems_r_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_exr_suggested = fields.Many2many('request.costing.item','exitems_r_suggested', string="Suggested", compute="_compute_items_stats")
    items_exr_failed = fields.Many2many('request.costing.item','exitems_r_failed', string="Failed", compute="_compute_items_stats")
    items_exr_required = fields.Many2many('request.costing.item','exitems_r_required', string="Required", compute="_compute_items_stats")
    items_exr_selected = fields.Many2many('request.costing.item','exitems_r_selected', string="Selected", compute="_compute_items_stats")
    items_exr_to_confirm = fields.Many2many('request.costing.item','exitems_r_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_exr_confirmed = fields.Many2many('request.costing.item','exitems_r_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_exr_to_bill = fields.Many2many('request.costing.item','exitems_r_to_bill', string="To Bill", compute="_compute_items_stats")
    items_exr_billed = fields.Many2many('request.costing.item','exitems_r_billed', string="Billed", compute="_compute_items_stats")

    items_exr_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_exr_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_exr_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_exr_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_exr_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_exr_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_exr_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_exr_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_exr_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_exr_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_exr_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_exr_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_exr_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_exr_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_exr_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_exr_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_exr_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_exr_requested_vendors = fields.Many2many('res.partner','exitems_r_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_exr_to_send_vendors = fields.Many2many('res.partner','exitems_r_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_exr_waiting_vendors = fields.Many2many('res.partner','exitems_r_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_exr_late_vendors = fields.Many2many('res.partner','exitems_r_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_exr_to_quote_vendors = fields.Many2many('res.partner','exitems_r_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_exr_quoted_vendors = fields.Many2many('res.partner','exitems_r_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_exr_quoted_high_vendors = fields.Many2many('res.partner','exitems_r_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_exr_quoted_low_vendors = fields.Many2many('res.partner','exitems_r_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_exr_suggested_vendors = fields.Many2many('res.partner','exitems_r_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_exr_failed_vendors = fields.Many2many('res.partner','exitems_r_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_exr_required_vendors = fields.Many2many('res.partner','exitems_r_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_exr_selected_vendors = fields.Many2many('res.partner','exitems_r_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_exr_to_confirm_vendors = fields.Many2many('res.partner','exitems_r_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_exr_confirmed_vendors = fields.Many2many('res.partner','exitems_r_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_exr_to_bill_vendors = fields.Many2many('res.partner','exitems_r_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_exr_billed_vendors = fields.Many2many('res.partner','exitems_r_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_exr_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_exr_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_exr_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_exr_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_exr_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_exr_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_exr_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_exr_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_exr_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_exr_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_exr_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_exr_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_exr_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_exr_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_exr_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_exr_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_exr_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_exr_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_exr_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_exr_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_exr_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_exr_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    # REQUESTED Internal Items Stats

    items_inr_requested = fields.Many2many('request.costing.item','initems_r_requested', string="Requested", compute="_compute_items_stats")
    items_inr_to_send = fields.Many2many('request.costing.item','initems_r_to_send', string="To Send", compute="_compute_items_stats")
    items_inr_waiting = fields.Many2many('request.costing.item','initems_r_waiting', string="Waiting", compute="_compute_items_stats")
    items_inr_late = fields.Many2many('request.costing.item','initems_r_late', string="Late", compute="_compute_items_stats")
    items_inr_to_quote = fields.Many2many('request.costing.item','initems_r_to_quote', string="To Quote", compute="_compute_items_stats")
    items_inr_quoted = fields.Many2many('request.costing.item','initems_r_quoted', string="Quoted", compute="_compute_items_stats")
    items_inr_quoted_high = fields.Many2many('request.costing.item','initems_r_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_inr_quoted_low = fields.Many2many('request.costing.item','initems_r_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_inr_suggested = fields.Many2many('request.costing.item','initems_r_suggested', string="Suggested", compute="_compute_items_stats")
    items_inr_failed = fields.Many2many('request.costing.item','initems_r_failed', string="Failed", compute="_compute_items_stats")
    items_inr_required = fields.Many2many('request.costing.item','initems_r_required', string="Required", compute="_compute_items_stats")
    items_inr_selected = fields.Many2many('request.costing.item','initems_r_selected', string="Selected", compute="_compute_items_stats")
    items_inr_to_confirm = fields.Many2many('request.costing.item','initems_r_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_inr_confirmed = fields.Many2many('request.costing.item','initems_r_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_inr_to_bill = fields.Many2many('request.costing.item','initems_r_to_bill', string="To Bill", compute="_compute_items_stats")
    items_inr_billed = fields.Many2many('request.costing.item','initems_r_billed', string="Billed", compute="_compute_items_stats")

    items_inr_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_inr_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_inr_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_inr_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_inr_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_inr_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_inr_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_inr_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_inr_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_inr_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_inr_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_inr_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_inr_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_inr_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_inr_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_inr_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_inr_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_inr_requested_vendors = fields.Many2many('res.partner','initems_r_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_inr_to_send_vendors = fields.Many2many('res.partner','initems_r_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_inr_waiting_vendors = fields.Many2many('res.partner','initems_r_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_inr_late_vendors = fields.Many2many('res.partner','initems_r_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_inr_to_quote_vendors = fields.Many2many('res.partner','initems_r_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_inr_quoted_vendors = fields.Many2many('res.partner','initems_r_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_inr_quoted_high_vendors = fields.Many2many('res.partner','initems_r_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_inr_quoted_low_vendors = fields.Many2many('res.partner','initems_r_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_inr_suggested_vendors = fields.Many2many('res.partner','initems_r_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_inr_failed_vendors = fields.Many2many('res.partner','initems_r_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_inr_required_vendors = fields.Many2many('res.partner','initems_r_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_inr_selected_vendors = fields.Many2many('res.partner','initems_r_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_inr_to_confirm_vendors = fields.Many2many('res.partner','initems_r_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_inr_confirmed_vendors = fields.Many2many('res.partner','initems_r_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_inr_to_bill_vendors = fields.Many2many('res.partner','initems_r_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_inr_billed_vendors = fields.Many2many('res.partner','initems_r_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_inr_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_inr_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_inr_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_inr_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_inr_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_inr_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_inr_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_inr_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_inr_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_inr_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_inr_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_inr_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_inr_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_inr_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_inr_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_inr_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_inr_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_inr_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_inr_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_inr_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_inr_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_inr_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    # REQUESTED Total Items Stats

    items_r_requested = fields.Many2many('request.costing.item','items_requested', string="Requested", compute="_compute_items_stats")
    items_r_to_send = fields.Many2many('request.costing.item','items_to_send', string="To Send", compute="_compute_items_stats")
    items_r_waiting = fields.Many2many('request.costing.item','items_waiting', string="Waiting", compute="_compute_items_stats")
    items_r_late = fields.Many2many('request.costing.item','items_late', string="Late", compute="_compute_items_stats")
    items_r_to_quote = fields.Many2many('request.costing.item','items_to_quote', string="To Quote", compute="_compute_items_stats")
    items_r_quoted = fields.Many2many('request.costing.item','items_quoted', string="Quoted", compute="_compute_items_stats")
    items_r_quoted_high = fields.Many2many('request.costing.item','items_high_quoted', string="Quoted High", compute="_compute_items_stats")
    items_r_quoted_low = fields.Many2many('request.costing.item','items_low_quoted', string="Quoted Low", compute="_compute_items_stats")
    items_r_suggested = fields.Many2many('request.costing.item','items_suggested', string="Suggested", compute="_compute_items_stats")
    items_r_failed = fields.Many2many('request.costing.item','items_failed', string="Failed", compute="_compute_items_stats")
    items_r_required = fields.Many2many('request.costing.item','items_required', string="Required", compute="_compute_items_stats")
    items_r_selected = fields.Many2many('request.costing.item','items_selected', string="Selected", compute="_compute_items_stats")
    items_r_to_confirm = fields.Many2many('request.costing.item','items_to_confirm', string="To Confirm", compute="_compute_items_stats")
    items_r_confirmed = fields.Many2many('request.costing.item','items_confirmed', string="Confirmed", compute="_compute_items_stats")
    items_r_to_bill = fields.Many2many('request.costing.item','items_to_bill', string="To Bill", compute="_compute_items_stats")
    items_r_billed = fields.Many2many('request.costing.item','items_billed', string="Billed", compute="_compute_items_stats")

    items_r_count = fields.Integer(string="Count", compute="_compute_items_stats")
    items_r_requested_count = fields.Integer(string="RFQs Requested Count", compute="_compute_items_stats")
    items_r_to_send_count = fields.Integer(string="To Send Count", compute="_compute_items_stats")
    items_r_waiting_count = fields.Integer(string="Waiting Count", compute="_compute_items_stats")   
    items_r_late_count = fields.Integer(string="Late Count", compute="_compute_items_stats")   
    items_r_to_quote_count = fields.Integer(string="To Quote Count", compute="_compute_items_stats")   
    items_r_quoted_count = fields.Integer(string="Quoted Count", compute="_compute_items_stats")   
    items_r_quoted_high_count = fields.Integer(string="Quoted High Count", compute="_compute_items_stats")   
    items_r_quoted_low_count = fields.Integer(string="Quoted Low Count", compute="_compute_items_stats")   
    items_r_suggested_count = fields.Integer(string="Suggested Count", compute="_compute_items_stats")   
    items_r_failed_count = fields.Integer(string="Failed Count", compute="_compute_items_stats")   
    items_r_required_count = fields.Integer(string="Required Count", compute="_compute_items_stats")   
    items_r_selected_count = fields.Integer(string="Selected Count", compute="_compute_items_stats")   
    items_r_to_confirm_count = fields.Integer(string="To Confirm Count", compute="_compute_items_stats")   
    items_r_confirmed_count = fields.Integer(string="Confirmed Count", compute="_compute_items_stats") 
    items_r_to_bill_count = fields.Integer(string="To Bill Count", compute="_compute_items_stats")
    items_r_billed_count = fields.Integer(string="Billed Count", compute="_compute_items_stats") 

    items_r_requested_vendors = fields.Many2many('res.partner','items_vendors_requested', string="Requested Vendors", compute="_compute_items_stats")
    items_r_to_send_vendors = fields.Many2many('res.partner','items_vendors_to_send', string="To Send Vendors", compute="_compute_items_stats")
    items_r_waiting_vendors = fields.Many2many('res.partner','items_vendors_waiting', string="Waiting Vendors", compute="_compute_items_stats")
    items_r_late_vendors = fields.Many2many('res.partner','items_vendors_late', string="Late Vendors", compute="_compute_items_stats")
    items_r_to_quote_vendors = fields.Many2many('res.partner','items_vendors_to_quote', string="To Quote Vendors", compute="_compute_items_stats")
    items_r_quoted_vendors = fields.Many2many('res.partner','items_vendors_quoted', string="Quoted Vendors", compute="_compute_items_stats")
    items_r_quoted_high_vendors = fields.Many2many('res.partner','items_vendors_high_quoted', string="Quoted High Vendors", compute="_compute_items_stats")
    items_r_quoted_low_vendors = fields.Many2many('res.partner','items_vendors_low_quoted', string="Quoted Low Vendors", compute="_compute_items_stats")
    items_r_suggested_vendors = fields.Many2many('res.partner','items_vendors_suggested', string="Suggested Vendors", compute="_compute_items_stats")
    items_r_failed_vendors = fields.Many2many('res.partner','items_vendors_failed', string="Failed Vendors", compute="_compute_items_stats")
    items_r_required_vendors = fields.Many2many('res.partner','items_vendors_required', string="Required Vendors", compute="_compute_items_stats")
    items_r_selected_vendors = fields.Many2many('res.partner','items_vendors_selected', string="Selected Vendors", compute="_compute_items_stats")
    items_r_to_confirm_vendors = fields.Many2many('res.partner','items_vendors_to_confirm', string="To Confirm Vendors", compute="_compute_items_stats")
    items_r_confirmed_vendors = fields.Many2many('res.partner','items_vendors_confirmed', string="Confirmed Vendors", compute="_compute_items_stats")
    items_r_to_bill_vendors = fields.Many2many('res.partner','items_vendors_to_bill', string="To Bill Vendors", compute="_compute_items_stats")
    items_r_billed_vendors = fields.Many2many('res.partner','items_vendors_billed', string="Billed Vendors", compute="_compute_items_stats")
    
    items_r_quoted_average = fields.Monetary(string="Quoted Average", compute="_compute_items_stats") 
    items_r_quoted_high_amount_applicable = fields.Monetary(string="Quoted High Applicable Amount", compute="_compute_items_stats")
    items_r_quoted_high_amount_total = fields.Monetary(string="Quoted High Total", compute="_compute_items_stats")
    items_r_quoted_high_amount_untaxed = fields.Monetary(string="Quoted High Untaxed", compute="_compute_items_stats")
    items_r_quoted_low_amount_applicable = fields.Monetary(string="Quoted Low Applicable Amount", compute="_compute_items_stats")
    items_r_quoted_low_amount_total = fields.Monetary(string="Quoted Low Total", compute="_compute_items_stats")
    items_r_quoted_low_amount_untaxed = fields.Monetary(string="Quoted Low Untaxed", compute="_compute_items_stats")
    items_r_required_total_applicable = fields.Monetary(string="Required Applicable Total", compute="_compute_items_stats")
    items_r_required_total_total = fields.Monetary(string="Required Total", compute="_compute_items_stats")
    items_r_required_total_untaxed = fields.Monetary(string="Required Untaxed", compute="_compute_items_stats")
    items_r_selected_total_applicable = fields.Monetary(string="Selected Applicable Total", compute="_compute_items_stats")
    items_r_selected_total_applicable_of_total = fields.Float(string="Selected Applicable Total Of Total", compute="_compute_items_stats")
    items_r_selected_total_applicable_of_target = fields.Float(string="Selected Applicable Total Of Target", compute="_compute_items_stats")
    items_r_selected_total_applicable_of_target_abs = fields.Float(string="Selected Applicable Total Of Target ABS", compute="_compute_items_stats")
    items_r_selected_total_total = fields.Monetary(string="Selected Total", compute="_compute_items_stats")
    items_r_selected_total_untaxed = fields.Monetary(string="Selected Untaxed", compute="_compute_items_stats")
    items_r_confirmed_total_applicable = fields.Monetary(string="Confirmed Applicable Total", compute="_compute_items_stats")
    items_r_confirmed_total_total = fields.Monetary(string="Confirmed Total", compute="_compute_items_stats")
    items_r_confirmed_total_untaxed = fields.Monetary(string="Confirmed Untaxed", compute="_compute_items_stats")
    items_r_billed_total_applicable = fields.Monetary(string="Billed Applicable Total", compute="_compute_items_stats")
    items_r_billed_total_total = fields.Monetary(string="Billed Total", compute="_compute_items_stats")
    items_r_billed_total_untaxed = fields.Monetary(string="Billed Untaxed", compute="_compute_items_stats")

    


    @api.depends('request_item_ids')
    def _compute_items_stats(self):
        for record in self:
            ## ALL ITEMS

            # ALL External Items Stats

            record.items_ex_requested = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.requested)
            record.items_ex_to_send = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.to_send)
            record.items_ex_waiting = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.waiting)
            record.items_ex_late = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.late)
            record.items_ex_quoted = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'quoted')
            record.items_ex_to_quote = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_quote')
            highest_ex_quoted_amount = record.items_ex_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_ex_quoted else False
            record.items_ex_quoted_high = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_ex_quoted_amount)
            lowest_ex_quoted_amount = record.items_ex_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_ex_quoted else False
            record.items_ex_quoted_low = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_ex_quoted_amount)
            record.items_ex_suggested = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'suggested')
            record.items_ex_failed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'failed')
            record.items_ex_required = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'required')
            record.items_ex_selected = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'selected')
            record.items_ex_to_confirm = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_confirm')
            record.items_ex_confirmed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'confirmed')
            record.items_ex_to_bill = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_bill')
            record.items_ex_billed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'billed')

            record.items_ex_count = len(record.request_item_ids.filtered(lambda r: r.type == 'external'))
            record.items_ex_requested_count = len(record.items_ex_requested)
            record.items_ex_to_send_count = len(record.items_ex_to_send)
            record.items_ex_waiting_count = len(record.items_ex_waiting)
            record.items_ex_late_count = len(record.items_ex_late)
            record.items_ex_to_quote_count = len(record.items_ex_to_quote)
            record.items_ex_quoted_count = len(record.items_ex_quoted)
            record.items_ex_quoted_high_count = len(record.items_ex_quoted_high)
            record.items_ex_quoted_low_count = len(record.items_ex_quoted_low)
            record.items_ex_suggested_count = len(record.items_ex_suggested)
            record.items_ex_failed_count = len(record.items_ex_failed)
            record.items_ex_required_count = len(record.items_ex_required)
            record.items_ex_selected_count = len(record.items_ex_selected)
            record.items_ex_to_confirm_count = len(record.items_ex_to_confirm)
            record.items_ex_confirmed_count = len(record.items_ex_confirmed)
            record.items_ex_to_bill_count = len(record.items_ex_to_bill)
            record.items_ex_billed_count = len(record.items_ex_billed)

            record.items_ex_requested_vendors = record.items_ex_requested.vendor_id.ids
            record.items_ex_to_send_vendors = record.items_ex_to_send.vendor_id.ids
            record.items_ex_waiting_vendors = record.items_ex_waiting.vendor_id.ids
            record.items_ex_late_vendors = record.items_ex_late.vendor_id.ids
            record.items_ex_to_quote_vendors = record.items_ex_to_quote.vendor_id.ids
            record.items_ex_quoted_vendors = record.items_ex_quoted.vendor_id.ids
            record.items_ex_quoted_high_vendors = record.items_ex_quoted_high.vendor_id.ids
            record.items_ex_quoted_low_vendors = record.items_ex_quoted_low.vendor_id.ids
            record.items_ex_suggested_vendors = record.items_ex_suggested.vendor_id.ids
            record.items_ex_failed_vendors = record.items_ex_failed.vendor_id.ids
            record.items_ex_required_vendors = record.items_ex_required.vendor_id.ids
            record.items_ex_selected_vendors = record.items_ex_selected.vendor_id.ids
            record.items_ex_to_confirm_vendors = record.items_ex_to_confirm.vendor_id.ids
            record.items_ex_confirmed_vendors = record.items_ex_confirmed.vendor_id.ids
            record.items_ex_to_bill_vendors = record.items_ex_to_bill.vendor_id.ids
            record.items_ex_billed_vendors = record.items_ex_billed.vendor_id.ids

            record.items_ex_quoted_average = (sum(item.applicable_co_total for item in record.items_ex_quoted) / record.items_ex_quoted_count) if record.items_ex_quoted else 0
            record.items_ex_quoted_high_amount_applicable = record.items_ex_quoted_high[0].applicable_co_total if record.items_ex_quoted_high else 0
            record.items_ex_quoted_high_amount_total = record.items_ex_quoted_high[0].applicable_co_taxed if record.items_ex_quoted_high else 0
            record.items_ex_quoted_high_amount_untaxed = record.items_ex_quoted_high[0].applicable_co_untaxed if record.items_ex_quoted_high else 0
            record.items_ex_quoted_low_amount_applicable = record.items_ex_quoted_low[0].applicable_co_total if record.items_ex_quoted_low else 0
            record.items_ex_quoted_low_amount_total = record.items_ex_quoted_low[0].applicable_co_taxed if record.items_ex_quoted_low else 0
            record.items_ex_quoted_low_amount_untaxed = record.items_ex_quoted_low[0].applicable_co_untaxed if record.items_ex_quoted_low else 0
            record.items_ex_required_total_applicable = sum(item.applicable_co_total for item in record.items_ex_required)
            record.items_ex_required_total_total = sum(item.applicable_co_taxed for item in record.items_ex_required)
            record.items_ex_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_ex_required)
            record.items_ex_selected_total_applicable = sum(item.applicable_co_total for item in record.items_ex_selected)
            
            
            record.items_ex_selected_total_total = sum(item.applicable_co_taxed for item in record.items_ex_selected)
            record.items_ex_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_ex_selected)
            record.items_ex_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_ex_confirmed)
            record.items_ex_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_ex_confirmed)
            record.items_ex_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_ex_confirmed)
            record.items_ex_billed_total_applicable = sum(item.applicable_co_total for item in record.items_ex_billed)
            record.items_ex_billed_total_total = sum(item.applicable_co_taxed for item in record.items_ex_billed)
            record.items_ex_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_ex_billed)

            # ALL Internal Items Stats

            record.items_in_requested = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.requested)
            record.items_in_to_send = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.to_send)
            record.items_in_waiting = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.waiting)
            record.items_in_late = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.late)
            record.items_in_quoted = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'quoted')
            record.items_in_to_quote = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_quote')
            highest_in_quoted_amount = record.items_in_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_in_quoted else False
            record.items_in_quoted_high = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_in_quoted_amount)
            lowest_in_quoted_amount = record.items_in_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_in_quoted else False
            record.items_in_quoted_low = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_in_quoted_amount)
            record.items_in_suggested = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'suggested')
            record.items_in_failed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'failed')
            record.items_in_required = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'required')
            record.items_in_selected = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'selected')
            record.items_in_to_confirm = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_confirm')
            record.items_in_confirmed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'confirmed')
            record.items_in_to_bill = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_bill')
            record.items_in_billed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'billed')

            record.items_product_in_requested = record.items_in_requested.product_id.ids
            record.items_product_in_quoted = record.items_in_quoted.product_id.ids
            record.items_product_in_suggested = record.items_in_suggested.product_id.ids
            record.items_product_in_failed = record.items_in_failed.product_id.ids
            record.items_product_in_required = record.items_in_required.product_id.ids
            record.items_product_in_selected = record.items_in_selected.product_id.ids
            record.items_product_in_confirmed = record.items_in_confirmed.product_id.ids
            record.items_product_in_billed = record.items_in_billed.product_id.ids

            record.items_in_count = len(record.request_item_ids.filtered(lambda r: r.type == 'internal'))
            record.items_in_requested_count = len(record.items_in_requested)
            record.items_in_to_send_count = len(record.items_in_to_send)
            record.items_in_waiting_count = len(record.items_in_waiting)
            record.items_in_late_count = len(record.items_in_late)
            record.items_in_to_quote_count = len(record.items_in_to_quote)
            record.items_in_quoted_count = len(record.items_in_quoted)
            record.items_in_quoted_high_count = len(record.items_in_quoted_high)
            record.items_in_quoted_low_count = len(record.items_in_quoted_low)
            record.items_in_suggested_count = len(record.items_in_suggested)
            record.items_in_failed_count = len(record.items_in_failed)
            record.items_in_required_count = len(record.items_in_required)
            record.items_in_selected_count = len(record.items_in_selected)
            record.items_in_to_confirm_count = len(record.items_in_to_confirm)
            record.items_in_confirmed_count = len(record.items_in_confirmed)
            record.items_in_to_bill_count = len(record.items_in_to_bill)
            record.items_in_billed_count = len(record.items_in_billed)

            record.items_in_requested_vendors = record.items_in_requested.vendor_id.ids
            record.items_in_to_send_vendors = record.items_in_to_send.vendor_id.ids
            record.items_in_waiting_vendors = record.items_in_waiting.vendor_id.ids
            record.items_in_late_vendors = record.items_in_late.vendor_id.ids
            record.items_in_to_quote_vendors = record.items_in_to_quote.vendor_id.ids
            record.items_in_quoted_vendors = record.items_in_quoted.vendor_id.ids
            record.items_in_quoted_high_vendors = record.items_in_quoted_high.vendor_id.ids
            record.items_in_quoted_low_vendors = record.items_in_quoted_low.vendor_id.ids
            record.items_in_suggested_vendors = record.items_in_suggested.vendor_id.ids
            record.items_in_failed_vendors = record.items_in_failed.vendor_id.ids
            record.items_in_required_vendors = record.items_in_required.vendor_id.ids
            record.items_in_selected_vendors = record.items_in_selected.vendor_id.ids
            record.items_in_to_confirm_vendors = record.items_in_to_confirm.vendor_id.ids
            record.items_in_confirmed_vendors = record.items_in_confirmed.vendor_id.ids
            record.items_in_to_bill_vendors = record.items_in_to_bill.vendor_id.ids
            record.items_in_billed_vendors = record.items_in_billed.vendor_id.ids

            record.items_in_quoted_average = (sum(item.applicable_co_total for item in record.items_in_quoted) / record.items_in_quoted_count) if record.items_in_quoted else 0
            record.items_in_quoted_high_amount_applicable = record.items_in_quoted_high[0].applicable_co_total if record.items_in_quoted_high else 0
            record.items_in_quoted_high_amount_total = record.items_in_quoted_high[0].applicable_co_taxed if record.items_in_quoted_high else 0
            record.items_in_quoted_high_amount_untaxed = record.items_in_quoted_high[0].applicable_co_untaxed if record.items_in_quoted_high else 0
            record.items_in_quoted_low_amount_applicable = record.items_in_quoted_low[0].applicable_co_total if record.items_in_quoted_low else 0
            record.items_in_quoted_low_amount_total = record.items_in_quoted_low[0].applicable_co_taxed if record.items_in_quoted_low else 0
            record.items_in_quoted_low_amount_untaxed = record.items_in_quoted_low[0].applicable_co_untaxed if record.items_in_quoted_low else 0
            record.items_in_required_total_applicable = sum(item.applicable_co_total for item in record.items_in_required)
            record.items_in_required_total_total = sum(item.applicable_co_taxed for item in record.items_in_required)
            record.items_in_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_in_required)
            record.items_in_selected_total_applicable = sum(item.applicable_co_total for item in record.items_in_selected)
            
            record.items_in_selected_total_total = sum(item.applicable_co_taxed for item in record.items_in_selected)
            record.items_in_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_in_selected)
            record.items_in_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_in_confirmed)
            record.items_in_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_in_confirmed)
            record.items_in_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_in_confirmed)
            record.items_in_billed_total_applicable = sum(item.applicable_co_total for item in record.items_in_billed)
            record.items_in_billed_total_total = sum(item.applicable_co_taxed for item in record.items_in_billed)
            record.items_in_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_in_billed)

            # ALL All Items Stats

            record.items_requested = record.request_item_ids.filtered(lambda r: r.requested)
            record.items_to_send = record.request_item_ids.filtered(lambda r: r.to_send)
            record.items_waiting = record.request_item_ids.filtered(lambda r: r.waiting)
            record.items_late = record.request_item_ids.filtered(lambda r: r.late)
            record.items_quoted = record.request_item_ids.filtered(lambda r: r.state == 'quoted')
            record.items_to_quote = record.request_item_ids.filtered(lambda r: r.state == 'to_quote')
            highest_quoted_amount = record.items_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_quoted else False
            record.items_quoted_high = record.request_item_ids.filtered(lambda r: r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_quoted_amount)
            lowest_quoted_amount = record.items_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_quoted else False
            record.items_quoted_low = record.request_item_ids.filtered(lambda r: r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_quoted_amount)
            record.items_suggested = record.request_item_ids.filtered(lambda r: r.state == 'suggested')
            record.items_failed = record.request_item_ids.filtered(lambda r: r.state == 'failed')
            record.items_required = record.request_item_ids.filtered(lambda r: r.state == 'required')
            record.items_selected = record.request_item_ids.filtered(lambda r: r.state == 'selected')
            record.items_to_confirm = record.request_item_ids.filtered(lambda r: r.state == 'to_confirm')
            record.items_confirmed = record.request_item_ids.filtered(lambda r: r.state == 'confirmed')
            record.items_to_bill = record.request_item_ids.filtered(lambda r: r.state == 'to_bill')
            record.items_billed = record.request_item_ids.filtered(lambda r: r.state == 'billed')

            record.items_count = len(record.request_item_ids)
            record.items_requested_count = len(record.items_requested)
            record.items_to_send_count = len(record.items_to_send)
            record.items_waiting_count = len(record.items_waiting)
            record.items_late_count = len(record.items_late)
            record.items_to_quote_count = len(record.items_to_quote)
            record.items_quoted_count = len(record.items_quoted)
            record.items_quoted_high_count = len(record.items_quoted_high)
            record.items_quoted_low_count = len(record.items_quoted_low)
            record.items_suggested_count = len(record.items_suggested)
            record.items_failed_count = len(record.items_failed)
            record.items_required_count = len(record.items_required)
            record.items_selected_count = len(record.items_selected)
            record.items_to_confirm_count = len(record.items_to_confirm)
            record.items_confirmed_count = len(record.items_confirmed)
            record.items_to_bill_count = len(record.items_to_bill)
            record.items_billed_count = len(record.items_billed)

            record.items_requested_vendors = record.items_requested.vendor_id.ids
            record.items_to_send_vendors = record.items_to_send.vendor_id.ids
            record.items_waiting_vendors = record.items_waiting.vendor_id.ids
            record.items_late_vendors = record.items_late.vendor_id.ids
            record.items_to_quote_vendors = record.items_to_quote.vendor_id.ids
            record.items_quoted_vendors = record.items_quoted.vendor_id.ids
            record.items_quoted_high_vendors = record.items_quoted_high.vendor_id.ids
            record.items_quoted_low_vendors = record.items_quoted_low.vendor_id.ids
            record.items_suggested_vendors = record.items_suggested.vendor_id.ids
            record.items_failed_vendors = record.items_failed.vendor_id.ids
            record.items_required_vendors = record.items_required.vendor_id.ids
            record.items_selected_vendors = record.items_selected.vendor_id.ids
            record.items_to_confirm_vendors = record.items_to_confirm.vendor_id.ids
            record.items_confirmed_vendors = record.items_confirmed.vendor_id.ids
            record.items_to_bill_vendors = record.items_to_bill.vendor_id.ids
            record.items_billed_vendors = record.items_billed.vendor_id.ids

            record.items_quoted_average = (sum(item.applicable_co_total for item in record.items_quoted) / record.items_quoted_count) if record.items_quoted else 0
            record.items_quoted_high_amount_applicable = record.items_quoted_high[0].applicable_co_total if record.items_quoted_high else 0
            record.items_quoted_high_amount_total = record.items_quoted_high[0].applicable_co_taxed if record.items_quoted_high else 0
            record.items_quoted_high_amount_untaxed = record.items_quoted_high[0].applicable_co_untaxed if record.items_quoted_high else 0
            record.items_quoted_low_amount_applicable = record.items_quoted_low[0].applicable_co_total if record.items_quoted_low else 0
            record.items_quoted_low_amount_total = record.items_quoted_low[0].applicable_co_taxed if record.items_quoted_low else 0
            record.items_quoted_low_amount_untaxed = record.items_quoted_low[0].applicable_co_untaxed if record.items_quoted_low else 0
            record.items_required_total_applicable = sum(item.applicable_co_total for item in record.items_required)
            record.items_required_total_total = sum(item.applicable_co_taxed for item in record.items_required)
            record.items_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_required)
            record.items_selected_total_applicable = sum(item.applicable_co_total for item in record.items_selected)
            
            record.items_selected_total_total = sum(item.applicable_co_taxed for item in record.items_selected)
            record.items_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_selected)
            record.items_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_confirmed)
            record.items_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_confirmed)
            record.items_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_confirmed)
            record.items_billed_total_applicable = sum(item.applicable_co_total for item in record.items_billed)
            record.items_billed_total_total = sum(item.applicable_co_taxed for item in record.items_billed)
            record.items_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_billed)

            record.items_ex_selected_total_applicable_of_total = (record.items_ex_selected_total_applicable / record.items_selected_total_applicable) if record.items_selected_total_applicable > 0 else 0
            record.items_in_selected_total_applicable_of_total = (record.items_in_selected_total_applicable / record.items_selected_total_applicable) if record.items_selected_total_applicable > 0 else 0
            record.items_selected_total_applicable_of_total = (record.items_selected_total_applicable / record.items_selected_total_applicable) if record.items_selected_total_applicable > 0 else 0

            ## REQUESTED ITEMS

            # REQUESTED External Items Stats

            record.items_exr_requested = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.requested)
            record.items_exr_to_send = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.to_send and r.requested)
            record.items_exr_waiting = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.waiting and r.requested)
            record.items_exr_late = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.late and r.requested)
            record.items_exr_quoted = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.requested)
            record.items_exr_to_quote = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_quote' and r.requested)
            highest_ex_quoted_amount = record.items_exr_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_exr_quoted else False
            record.items_exr_quoted_high = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_ex_quoted_amount and r.requested)
            lowest_ex_quoted_amount = record.items_exr_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_exr_quoted else False
            record.items_exr_quoted_low = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_ex_quoted_amount and r.requested)
            record.items_exr_suggested = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'suggested' and r.requested)
            record.items_exr_failed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'failed' and r.requested)
            record.items_exr_required = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'required' and r.requested)
            record.items_exr_selected = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'selected' and r.requested)
            record.items_exr_to_confirm = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_confirm' and r.requested)
            record.items_exr_confirmed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'confirmed' and r.requested)
            record.items_exr_to_bill = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'to_bill' and r.requested)
            record.items_exr_billed = record.request_item_ids.filtered(lambda r: r.type == 'external' and r.state == 'billed' and r.requested)

            record.items_exr_count = len(record.request_item_ids.filtered(lambda r: r.type == 'external' and r.requested))
            record.items_exr_requested_count = len(record.items_exr_requested)
            record.items_exr_to_send_count = len(record.items_exr_to_send)
            record.items_exr_waiting_count = len(record.items_exr_waiting)
            record.items_exr_late_count = len(record.items_exr_late)
            record.items_exr_to_quote_count = len(record.items_exr_to_quote)
            record.items_exr_quoted_count = len(record.items_exr_quoted)
            record.items_exr_quoted_high_count = len(record.items_exr_quoted_high)
            record.items_exr_quoted_low_count = len(record.items_exr_quoted_low)
            record.items_exr_suggested_count = len(record.items_exr_suggested)
            record.items_exr_failed_count = len(record.items_exr_failed)
            record.items_exr_required_count = len(record.items_exr_required)
            record.items_exr_selected_count = len(record.items_exr_selected)
            record.items_exr_to_confirm_count = len(record.items_exr_to_confirm)
            record.items_exr_confirmed_count = len(record.items_exr_confirmed)
            record.items_exr_to_bill_count = len(record.items_exr_to_bill)
            record.items_exr_billed_count = len(record.items_exr_billed)

            record.items_exr_requested_vendors = record.items_exr_requested.vendor_id.ids
            record.items_exr_to_send_vendors = record.items_exr_to_send.vendor_id.ids
            record.items_exr_waiting_vendors = record.items_exr_waiting.vendor_id.ids
            record.items_exr_late_vendors = record.items_exr_late.vendor_id.ids
            record.items_exr_to_quote_vendors = record.items_exr_to_quote.vendor_id.ids
            record.items_exr_quoted_vendors = record.items_exr_quoted.vendor_id.ids
            record.items_exr_quoted_high_vendors = record.items_exr_quoted_high.vendor_id.ids
            record.items_exr_quoted_low_vendors = record.items_exr_quoted_low.vendor_id.ids
            record.items_exr_suggested_vendors = record.items_exr_suggested.vendor_id.ids
            record.items_exr_failed_vendors = record.items_exr_failed.vendor_id.ids
            record.items_exr_required_vendors = record.items_exr_required.vendor_id.ids
            record.items_exr_selected_vendors = record.items_exr_selected.vendor_id.ids
            record.items_exr_to_confirm_vendors = record.items_exr_to_confirm.vendor_id.ids
            record.items_exr_confirmed_vendors = record.items_exr_confirmed.vendor_id.ids
            record.items_exr_to_bill_vendors = record.items_exr_to_bill.vendor_id.ids
            record.items_exr_billed_vendors = record.items_exr_billed.vendor_id.ids

            record.items_exr_quoted_average = (sum(item.applicable_co_total for item in record.items_exr_quoted) / record.items_exr_quoted_count) if record.items_exr_quoted else 0
            record.items_exr_quoted_high_amount_applicable = record.items_exr_quoted_high[0].applicable_co_total if record.items_exr_quoted_high else 0
            record.items_exr_quoted_high_amount_total = record.items_exr_quoted_high[0].applicable_co_taxed if record.items_exr_quoted_high else 0
            record.items_exr_quoted_high_amount_untaxed = record.items_exr_quoted_high[0].applicable_co_untaxed if record.items_exr_quoted_high else 0
            record.items_exr_quoted_low_amount_applicable = record.items_exr_quoted_low[0].applicable_co_total if record.items_exr_quoted_low else 0
            record.items_exr_quoted_low_amount_total = record.items_exr_quoted_low[0].applicable_co_taxed if record.items_exr_quoted_low else 0
            record.items_exr_quoted_low_amount_untaxed = record.items_exr_quoted_low[0].applicable_co_untaxed if record.items_exr_quoted_low else 0
            record.items_exr_required_total_applicable = sum(item.applicable_co_total for item in record.items_exr_required)
            record.items_exr_required_total_total = sum(item.applicable_co_taxed for item in record.items_exr_required)
            record.items_exr_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_exr_required)
            record.items_exr_selected_total_applicable = sum(item.applicable_co_total for item in record.items_exr_selected)
            
            record.items_exr_selected_total_total = sum(item.applicable_co_taxed for item in record.items_exr_selected)
            record.items_exr_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_exr_selected)
            record.items_exr_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_exr_confirmed)
            record.items_exr_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_exr_confirmed)
            record.items_exr_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_exr_confirmed)
            record.items_exr_billed_total_applicable = sum(item.applicable_co_total for item in record.items_exr_billed)
            record.items_exr_billed_total_total = sum(item.applicable_co_taxed for item in record.items_exr_billed)
            record.items_exr_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_exr_billed)

            # REQUESTED Internal Items Stats

            record.items_inr_requested = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.requested)
            record.items_inr_to_send = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.to_send and r.requested)
            record.items_inr_waiting = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.waiting and r.requested)
            record.items_inr_late = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.late and r.requested)
            record.items_inr_quoted = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.requested)
            record.items_inr_to_quote = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_quote' and r.requested)
            highest_in_quoted_amount = record.items_inr_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_inr_quoted else False
            record.items_inr_quoted_high = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_in_quoted_amount and r.requested)
            lowest_in_quoted_amount = record.items_inr_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_inr_quoted else False
            record.items_inr_quoted_low = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_in_quoted_amount and r.requested)
            record.items_inr_suggested = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'suggested' and r.requested)
            record.items_inr_failed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'failed' and r.requested)
            record.items_inr_required = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'required' and r.requested)
            record.items_inr_selected = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'selected' and r.requested)
            record.items_inr_to_confirm = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_confirm' and r.requested)
            record.items_inr_confirmed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'confirmed' and r.requested)
            record.items_inr_to_bill = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'to_bill' and r.requested)
            record.items_inr_billed = record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.state == 'billed' and r.requested)

            record.items_inr_count = len(record.request_item_ids.filtered(lambda r: r.type == 'internal' and r.requested))
            record.items_inr_requested_count = len(record.items_inr_requested)
            record.items_inr_to_send_count = len(record.items_inr_to_send)
            record.items_inr_waiting_count = len(record.items_inr_waiting)
            record.items_inr_late_count = len(record.items_inr_late)
            record.items_inr_to_quote_count = len(record.items_inr_to_quote)
            record.items_inr_quoted_count = len(record.items_inr_quoted)
            record.items_inr_quoted_high_count = len(record.items_inr_quoted_high)
            record.items_inr_quoted_low_count = len(record.items_inr_quoted_low)
            record.items_inr_suggested_count = len(record.items_inr_suggested)
            record.items_inr_failed_count = len(record.items_inr_failed)
            record.items_inr_required_count = len(record.items_inr_required)
            record.items_inr_selected_count = len(record.items_inr_selected)
            record.items_inr_to_confirm_count = len(record.items_inr_to_confirm)
            record.items_inr_confirmed_count = len(record.items_inr_confirmed)
            record.items_inr_to_bill_count = len(record.items_inr_to_bill)
            record.items_inr_billed_count = len(record.items_inr_billed)

            record.items_inr_requested_vendors = record.items_inr_requested.vendor_id.ids
            record.items_inr_to_send_vendors = record.items_inr_to_send.vendor_id.ids
            record.items_inr_waiting_vendors = record.items_inr_waiting.vendor_id.ids
            record.items_inr_late_vendors = record.items_inr_late.vendor_id.ids
            record.items_inr_to_quote_vendors = record.items_inr_to_quote.vendor_id.ids
            record.items_inr_quoted_vendors = record.items_inr_quoted.vendor_id.ids
            record.items_inr_quoted_high_vendors = record.items_inr_quoted_high.vendor_id.ids
            record.items_inr_quoted_low_vendors = record.items_inr_quoted_low.vendor_id.ids
            record.items_inr_suggested_vendors = record.items_inr_suggested.vendor_id.ids
            record.items_inr_failed_vendors = record.items_inr_failed.vendor_id.ids
            record.items_inr_required_vendors = record.items_inr_required.vendor_id.ids
            record.items_inr_selected_vendors = record.items_inr_selected.vendor_id.ids
            record.items_inr_to_confirm_vendors = record.items_inr_to_confirm.vendor_id.ids
            record.items_inr_confirmed_vendors = record.items_inr_confirmed.vendor_id.ids
            record.items_inr_to_bill_vendors = record.items_inr_to_bill.vendor_id.ids
            record.items_inr_billed_vendors = record.items_inr_billed.vendor_id.ids

            record.items_inr_quoted_average = (sum(item.applicable_co_total for item in record.items_inr_quoted) / record.items_inr_quoted_count) if record.items_inr_quoted else 0
            record.items_inr_quoted_high_amount_applicable = record.items_inr_quoted_high[0].applicable_co_total if record.items_inr_quoted_high else 0
            record.items_inr_quoted_high_amount_total = record.items_inr_quoted_high[0].applicable_co_taxed if record.items_inr_quoted_high else 0
            record.items_inr_quoted_high_amount_untaxed = record.items_inr_quoted_high[0].applicable_co_untaxed if record.items_inr_quoted_high else 0
            record.items_inr_quoted_low_amount_applicable = record.items_inr_quoted_low[0].applicable_co_total if record.items_inr_quoted_low else 0
            record.items_inr_quoted_low_amount_total = record.items_inr_quoted_low[0].applicable_co_taxed if record.items_inr_quoted_low else 0
            record.items_inr_quoted_low_amount_untaxed = record.items_inr_quoted_low[0].applicable_co_untaxed if record.items_inr_quoted_low else 0
            record.items_inr_required_total_applicable = sum(item.applicable_co_total for item in record.items_inr_required)
            record.items_inr_required_total_total = sum(item.applicable_co_taxed for item in record.items_inr_required)
            record.items_inr_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_inr_required)
            record.items_inr_selected_total_applicable = sum(item.applicable_co_total for item in record.items_inr_selected)
            
            record.items_inr_selected_total_total = sum(item.applicable_co_taxed for item in record.items_inr_selected)
            record.items_inr_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_inr_selected)
            record.items_inr_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_inr_confirmed)
            record.items_inr_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_inr_confirmed)
            record.items_inr_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_inr_confirmed)
            record.items_inr_billed_total_applicable = sum(item.applicable_co_total for item in record.items_inr_billed)
            record.items_inr_billed_total_total = sum(item.applicable_co_taxed for item in record.items_inr_billed)
            record.items_inr_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_inr_billed)

            # REQUESTED All Items Stats

            record.items_r_requested = record.request_item_ids.filtered(lambda r: r.requested)
            record.items_r_to_send = record.request_item_ids.filtered(lambda r: r.to_send and r.requested)
            record.items_r_waiting = record.request_item_ids.filtered(lambda r: r.waiting and r.requested)
            record.items_r_late = record.request_item_ids.filtered(lambda r: r.late and r.requested)
            record.items_r_quoted = record.request_item_ids.filtered(lambda r: r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.requested)
            record.items_r_to_quote = record.request_item_ids.filtered(lambda r: r.state == 'to_quote' and r.requested)
            highest_quoted_amount = record.items_r_quoted.sorted(key=lambda r: r.applicable_co_total, reverse=True)[0].applicable_co_total if record.items_r_quoted else False
            record.items_r_quoted_high = record.request_item_ids.filtered(lambda r: r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == highest_quoted_amount and r.requested)
            lowest_quoted_amount = record.items_r_quoted.sorted(key=lambda r: r.applicable_co_total)[0].applicable_co_total if record.items_r_quoted else False
            record.items_r_quoted_low = record.request_item_ids.filtered(lambda r: r.state not in ['draft','to_quote','to_validate','to_validate_failed','failed','cancel'] and r.applicable_co_total == lowest_quoted_amount and r.requested)
            record.items_r_suggested = record.request_item_ids.filtered(lambda r: r.state == 'suggested' and r.requested)
            record.items_r_failed = record.request_item_ids.filtered(lambda r: r.state == 'failed' and r.requested)
            record.items_r_required = record.request_item_ids.filtered(lambda r: r.state == 'required' and r.requested)
            record.items_r_selected = record.request_item_ids.filtered(lambda r: r.state == 'selected' and r.requested)
            record.items_r_to_confirm = record.request_item_ids.filtered(lambda r: r.state == 'to_confirm' and r.requested)
            record.items_r_confirmed = record.request_item_ids.filtered(lambda r: r.state == 'confirmed' and r.requested)
            record.items_r_to_bill = record.request_item_ids.filtered(lambda r: r.state == 'to_bill' and r.requested)
            record.items_r_billed = record.request_item_ids.filtered(lambda r: r.state == 'billed' and r.requested)

            record.items_r_count = len(record.request_item_ids.filtered(lambda r: r.requested))
            record.items_r_requested_count = len(record.items_r_requested)
            record.items_r_to_send_count = len(record.items_r_to_send)
            record.items_r_waiting_count = len(record.items_r_waiting)
            record.items_r_late_count = len(record.items_r_late)
            record.items_r_to_quote_count = len(record.items_r_to_quote)
            record.items_r_quoted_count = len(record.items_r_quoted)
            record.items_r_quoted_high_count = len(record.items_r_quoted_high)
            record.items_r_quoted_low_count = len(record.items_r_quoted_low)
            record.items_r_suggested_count = len(record.items_r_suggested)
            record.items_r_failed_count = len(record.items_r_failed)
            record.items_r_required_count = len(record.items_r_required)
            record.items_r_selected_count = len(record.items_r_selected)
            record.items_r_to_confirm_count = len(record.items_r_to_confirm)
            record.items_r_confirmed_count = len(record.items_r_confirmed)
            record.items_r_to_bill_count = len(record.items_r_to_bill)
            record.items_r_billed_count = len(record.items_r_billed)

            record.items_r_requested_vendors = record.items_r_requested.vendor_id.ids
            record.items_r_to_send_vendors = record.items_r_to_send.vendor_id.ids
            record.items_r_waiting_vendors = record.items_r_waiting.vendor_id.ids
            record.items_r_late_vendors = record.items_r_late.vendor_id.ids
            record.items_r_to_quote_vendors = record.items_r_to_quote.vendor_id.ids
            record.items_r_quoted_vendors = record.items_r_quoted.vendor_id.ids
            record.items_r_quoted_high_vendors = record.items_r_quoted_high.vendor_id.ids
            record.items_r_quoted_low_vendors = record.items_r_quoted_low.vendor_id.ids
            record.items_r_suggested_vendors = record.items_r_suggested.vendor_id.ids
            record.items_r_failed_vendors = record.items_r_failed.vendor_id.ids
            record.items_r_required_vendors = record.items_r_required.vendor_id.ids
            record.items_r_selected_vendors = record.items_r_selected.vendor_id.ids
            record.items_r_to_confirm_vendors = record.items_r_to_confirm.vendor_id.ids
            record.items_r_confirmed_vendors = record.items_r_confirmed.vendor_id.ids
            record.items_r_to_bill_vendors = record.items_r_to_bill.vendor_id.ids
            record.items_r_billed_vendors = record.items_r_billed.vendor_id.ids

            record.items_r_quoted_average = (sum(item.applicable_co_total for item in record.items_r_quoted) / record.items_r_quoted_count) if record.items_r_quoted else 0
            record.items_r_quoted_high_amount_applicable = record.items_r_quoted_high[0].applicable_co_total if record.items_r_quoted_high else 0
            record.items_r_quoted_high_amount_total = record.items_r_quoted_high[0].applicable_co_taxed if record.items_r_quoted_high else 0
            record.items_r_quoted_high_amount_untaxed = record.items_r_quoted_high[0].applicable_co_untaxed if record.items_r_quoted_high else 0
            record.items_r_quoted_low_amount_applicable = record.items_r_quoted_low[0].applicable_co_total if record.items_r_quoted_low else 0
            record.items_r_quoted_low_amount_total = record.items_r_quoted_low[0].applicable_co_taxed if record.items_r_quoted_low else 0
            record.items_r_quoted_low_amount_untaxed = record.items_r_quoted_low[0].applicable_co_untaxed if record.items_r_quoted_low else 0
            record.items_r_required_total_applicable = sum(item.applicable_co_total for item in record.items_r_required)
            record.items_r_required_total_total = sum(item.applicable_co_taxed for item in record.items_r_required)
            record.items_r_required_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_r_required)
            record.items_r_selected_total_applicable = sum(item.applicable_co_total for item in record.items_r_selected)
            
            record.items_r_selected_total_total = sum(item.applicable_co_taxed for item in record.items_r_selected)
            record.items_r_selected_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_r_selected)
            record.items_r_confirmed_total_applicable = sum(item.applicable_co_total for item in record.items_r_confirmed)
            record.items_r_confirmed_total_total = sum(item.applicable_co_taxed for item in record.items_r_confirmed)
            record.items_r_confirmed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_r_confirmed)
            record.items_r_billed_total_applicable = sum(item.applicable_co_total for item in record.items_r_billed)
            record.items_r_billed_total_total = sum(item.applicable_co_taxed for item in record.items_r_billed)
            record.items_r_billed_total_untaxed = sum(item.applicable_co_untaxed for item in record.items_r_billed)



            # summary
            record.items_exr_selected_total_applicable_of_total = (record.items_exr_selected_total_applicable / record.items_r_selected_total_applicable) if record.items_r_selected_total_applicable > 0 else 0
            record.items_inr_selected_total_applicable_of_total = (record.items_inr_selected_total_applicable / record.items_r_selected_total_applicable) if record.items_r_selected_total_applicable > 0 else 0
            record.items_r_selected_total_applicable_of_total = (record.items_r_selected_total_applicable / record.items_r_selected_total_applicable) if record.items_r_selected_total_applicable > 0 else 0

            record.items_ex_selected_total_applicable_of_target = ((record.items_ex_selected_total_applicable - record.target_cost) / record.target_cost) if record.target_cost > 0 else 0
            record.items_in_selected_total_applicable_of_target = ((record.items_in_selected_total_applicable - record.target_cost) / record.target_cost) if record.target_cost > 0 else 0
            record.items_selected_total_applicable_of_target = ((record.items_selected_total_applicable - record.target_cost) / record.target_cost) if record.target_cost > 0 else 0

            record.items_exr_selected_total_applicable_of_target = (record.items_exr_selected_total_applicable / record.target_cost) if record.target_cost > 0 else 0
            record.items_inr_selected_total_applicable_of_target = (record.items_inr_selected_total_applicable / record.target_cost) if record.target_cost > 0 else 0
            record.items_r_selected_total_applicable_of_target = (record.items_r_selected_total_applicable / record.target_cost) if record.target_cost > 0 else 0

            record.items_ex_selected_total_applicable_of_target_abs = abs(record.items_ex_selected_total_applicable_of_target)
            record.items_in_selected_total_applicable_of_target_abs = abs(record.items_in_selected_total_applicable_of_target)
            record.items_selected_total_applicable_of_target_abs = abs(record.items_selected_total_applicable_of_target)

            record.items_exr_selected_total_applicable_of_target_abs = abs(record.items_exr_selected_total_applicable_of_target)
            record.items_inr_selected_total_applicable_of_target_abs = abs(record.items_inr_selected_total_applicable_of_target)
            record.items_r_selected_total_applicable_of_target_abs = abs(record.items_r_selected_total_applicable_of_target)
            
    
    #view and filter fields
    stats_filter = fields.Selection([('all','All'),('external','External'),('internal','Internal')], default="all", store=False, string="Filter Type")
    
    stat_ex_bar_rank1_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_ex_bar_rank1_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_ex_bar_rank1_vendors = fields.Many2many('res.partner','costitem_rank1_vendors', compute="_compute_stat_bar_rank")
    stat_ex_bar_rank2_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_ex_bar_rank2_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_ex_bar_rank2_vendors = fields.Many2many('res.partner','costitem_rank2_vendors', compute="_compute_stat_bar_rank")
    stat_ex_bar_rank3_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_ex_bar_rank3_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_ex_bar_rank3_vendors = fields.Many2many('res.partner','costitem_rank3_vendors', compute="_compute_stat_bar_rank")
    stat_ex_bar_rank4_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_ex_bar_rank4_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_ex_bar_rank4_vendors = fields.Many2many('res.partner','costitem_rank4_vendors', compute="_compute_stat_bar_rank")

    stat_in_bar_rank1_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_in_bar_rank1_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_in_bar_rank1_vendors = fields.Many2many('res.partner','costitem_rank1_vendors', compute="_compute_stat_bar_rank")
    stat_in_bar_rank2_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_in_bar_rank2_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_in_bar_rank2_vendors = fields.Many2many('res.partner','costitem_rank2_vendors', compute="_compute_stat_bar_rank")
    stat_in_bar_rank3_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_in_bar_rank3_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_in_bar_rank3_vendors = fields.Many2many('res.partner','costitem_rank3_vendors', compute="_compute_stat_bar_rank")
    stat_in_bar_rank4_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_in_bar_rank4_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_in_bar_rank4_vendors = fields.Many2many('res.partner','costitem_rank4_vendors', compute="_compute_stat_bar_rank")

    stat_bar_rank1_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_bar_rank1_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_bar_rank1_vendors = fields.Many2many('res.partner','costitem_rank1_vendors', compute="_compute_stat_bar_rank")
    stat_bar_rank2_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_bar_rank2_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_bar_rank2_vendors = fields.Many2many('res.partner','costitem_rank2_vendors', compute="_compute_stat_bar_rank")
    stat_bar_rank3_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_bar_rank3_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_bar_rank3_vendors = fields.Many2many('res.partner','costitem_rank3_vendors', compute="_compute_stat_bar_rank")
    stat_bar_rank4_field = fields.Char(compute="_compute_stat_bar_rank")
    stat_bar_rank4_amount = fields.Integer(compute="_compute_stat_bar_rank", digits=0)
    stat_bar_rank4_vendors = fields.Many2many('res.partner','costitem_rank4_vendors', compute="_compute_stat_bar_rank")

    @api.depends('items_quoted_low','items_quoted_high','target_cost','items_requested','items_selected','items_selected_total_applicable')
    @api.onchange('items_quoted_low','items_quoted_high','target_cost','items_requested','items_selected','items_selected_total_applicable')
    def _compute_stat_bar_rank(self):
        for record in self:

            # ALL stats
            lowest_amount = int(record.items_quoted_low[0].applicable_co_total) if record.items_quoted_low else 0
            lowest_vendors = record.items_quoted_low_vendors
            highest_amount = int(record.items_quoted_high[0].applicable_co_total) if record.items_quoted_high else 0
            highest_vendors = record.items_quoted_high_vendors
            target_cost = int(record.target_cost)
            target_vendors = record.items_requested_vendors
            total_cost = int(record.items_selected_total_applicable)
            total_vendors = record.items_selected_vendors

            lowest = {"Item": "Lowest","Amount":lowest_amount,"Vendors":lowest_vendors}
            highest = {"Item": "Highest","Amount":highest_amount,"Vendors":highest_vendors}
            target = {"Item": "Target","Amount":target_cost,"Vendors":target_vendors}
            selected = {"Item": "Selected","Amount":total_cost,"Vendors":total_vendors}

            list_items = []
            list_items.append(lowest)
            list_items.append(highest)
            list_items.append(target)
            list_items.append(selected)

            sorted_list_items = sorted(list_items, key=lambda d: d['Amount']) 

            record.stat_bar_rank1_field = sorted_list_items[0]['Item']
            record.stat_bar_rank1_amount = sorted_list_items[0]['Amount']
            record.stat_bar_rank1_vendors = sorted_list_items[0]['Vendors']

            record.stat_bar_rank2_field = sorted_list_items[1]['Item']
            record.stat_bar_rank2_amount = sorted_list_items[1]['Amount']
            record.stat_bar_rank2_vendors = sorted_list_items[1]['Vendors']

            record.stat_bar_rank3_field = sorted_list_items[2]['Item']
            record.stat_bar_rank3_amount = sorted_list_items[2]['Amount']
            record.stat_bar_rank3_vendors = sorted_list_items[2]['Vendors']

            record.stat_bar_rank4_field = sorted_list_items[3]['Item']
            record.stat_bar_rank4_amount = sorted_list_items[3]['Amount']
            record.stat_bar_rank4_vendors = sorted_list_items[3]['Vendors']

            # External stats
            lowest_ex_amount = int(record.items_ex_quoted_low[0].applicable_co_total) if record.items_ex_quoted_low else 0
            lowest_ex_vendors = record.items_ex_quoted_low_vendors
            highest_ex_amount = int(record.items_ex_quoted_high[0].applicable_co_total) if record.items_ex_quoted_high else 0
            highest_ex_vendors = record.items_ex_quoted_high_vendors
            target_cost = int(record.target_cost)
            target_ex_vendors = record.items_ex_requested_vendors
            total_ex_cost = int(record.items_ex_selected_total_applicable)
            total_ex_vendors = record.items_ex_selected_vendors

            lowest_ex = {"Item": "Lowest","Amount":lowest_ex_amount,"Vendors":lowest_ex_vendors}
            highest_ex = {"Item": "Highest","Amount":highest_ex_amount,"Vendors":highest_ex_vendors}
            target_ex = {"Item": "Target","Amount":target_cost,"Vendors":target_ex_vendors}
            selected_ex = {"Item": "Selected","Amount":total_ex_cost,"Vendors":total_ex_vendors}

            list_ex_items = []
            list_ex_items.append(lowest_ex)
            list_ex_items.append(highest_ex)
            list_ex_items.append(target_ex)
            list_ex_items.append(selected_ex)

            sorted_list_ex_items = sorted(list_ex_items, key=lambda d: d['Amount']) 

            record.stat_ex_bar_rank1_field = sorted_list_ex_items[0]['Item']
            record.stat_ex_bar_rank1_amount = sorted_list_ex_items[0]['Amount']
            record.stat_ex_bar_rank1_vendors = sorted_list_ex_items[0]['Vendors']

            record.stat_ex_bar_rank2_field = sorted_list_ex_items[1]['Item']
            record.stat_ex_bar_rank2_amount = sorted_list_ex_items[1]['Amount']
            record.stat_ex_bar_rank2_vendors = sorted_list_ex_items[1]['Vendors']

            record.stat_ex_bar_rank3_field = sorted_list_ex_items[2]['Item']
            record.stat_ex_bar_rank3_amount = sorted_list_ex_items[2]['Amount']
            record.stat_ex_bar_rank3_vendors = sorted_list_ex_items[2]['Vendors']

            record.stat_ex_bar_rank4_field = sorted_list_ex_items[3]['Item']
            record.stat_ex_bar_rank4_amount = sorted_list_ex_items[3]['Amount']
            record.stat_ex_bar_rank4_vendors = sorted_list_ex_items[3]['Vendors']

            # Internal stats
            lowest_in_amount = int(record.items_in_quoted_low[0].applicable_co_total) if record.items_in_quoted_low else 0
            lowest_in_vendors = record.items_in_quoted_low_vendors
            highest_in_amount = int(record.items_in_quoted_high[0].applicable_co_total) if record.items_in_quoted_high else 0
            highest_in_vendors = record.items_in_quoted_high_vendors
            target_cost = int(record.target_cost)
            target_in_vendors = record.items_in_requested_vendors
            total_in_cost = int(record.items_in_selected_total_applicable)
            total_in_vendors = record.items_in_selected_vendors

            lowest_in = {"Item": "Lowest","Amount":lowest_in_amount,"Vendors":lowest_in_vendors}
            highest_in = {"Item": "Highest","Amount":highest_in_amount,"Vendors":highest_in_vendors}
            target_in = {"Item": "Target","Amount":target_cost,"Vendors":target_in_vendors}
            selected_in = {"Item": "Selected","Amount":total_in_cost,"Vendors":total_in_vendors}

            list_in_items = []
            list_in_items.append(lowest_in)
            list_in_items.append(highest_in)
            list_in_items.append(target_in)
            list_in_items.append(selected_in)

            sorted_list_in_items = sorted(list_in_items, key=lambda d: d['Amount']) 

            record.stat_in_bar_rank1_field = sorted_list_in_items[0]['Item']
            record.stat_in_bar_rank1_amount = sorted_list_in_items[0]['Amount']
            record.stat_in_bar_rank1_vendors = sorted_list_in_items[0]['Vendors']

            record.stat_in_bar_rank2_field = sorted_list_in_items[1]['Item']
            record.stat_in_bar_rank2_amount = sorted_list_in_items[1]['Amount']
            record.stat_in_bar_rank2_vendors = sorted_list_in_items[1]['Vendors']

            record.stat_in_bar_rank3_field = sorted_list_in_items[2]['Item']
            record.stat_in_bar_rank3_amount = sorted_list_in_items[2]['Amount']
            record.stat_in_bar_rank3_vendors = sorted_list_in_items[2]['Vendors']

            record.stat_in_bar_rank4_field = sorted_list_in_items[3]['Item']
            record.stat_in_bar_rank4_amount = sorted_list_in_items[3]['Amount']
            record.stat_in_bar_rank4_vendors = sorted_list_in_items[3]['Vendors']
            






    #tickets fields
    ticket_ids = fields.One2many('ticket','request_costing_id', string="Tickets", auto_join=True)

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.id))),('state','=','open'),('action','in',['req_cost_submit','req_cost_resubmit'])])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)

            
            # add pending tickets for team_id team leader
            user_ids = record.requester_ou_id.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing', record.id)),
                        'request_costing_id': record.id,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_sale',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    #record.write({'ticket_ids': [(0, 0, datas)]})
                    new_ticket = self.env['ticket'].create(datas)
                    #record.offer_notes = str(datas)
                    #record.request_notes = str(new_ticket)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})

    def action_wizard_validate_sale(self):
        
        return {
            'name': 'Validate Request(s)',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_validate_sale'
                }
        }

    def _action_validate_sale(self, note=False):
        for record in self:
            record.write({'state': 'costing'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_sale')
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.id))),('state','=','open'),('action','=','req_cost_validate_sale')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket(s) for each requested item's assigned user to request ticket_ids and item ticket_ids

            if record.request_item_ids:
                for item in record.request_item_ids:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing.item', item.id)),
                        'request_costing_id': record.id,
                        'user_id': item.assigned_user_id.id,
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state':'open',
                    }
                    new_ticket = self.env['ticket'].create(datas)
                    #item.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #item.ticket_ids = [(4, new_ticket.id)]
                    #record.ticket_ids = [(4, new_ticket.id)]

    def action_wizard_return_sale(self):

        return {
            'name': 'Return Request(s)',
            'view_mode': 'form',
            'res_model': 'request.costing.user.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_request_ids': self.ids,
                'default_name': 'req_cost_return_sale'
                }
        }

    def _action_return_sale(self, note=False):
        for record in self:
            record.write({'state': 'draft'})
            
            #close current related tickets and add note
            #related_ticket_ids = record.ticket_ids.filtered(lambda r: r.state == 'open' and r.action == 'req_cost_validate_sale')
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.id))),('state','=','open'),('action','=','req_cost_validate_sale')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                        'user_id': user.id,                        
                        'action':'req_cost_resubmit',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    #record.write({'ticket_ids': [(0, 0, datas)]})
                    new_ticket = self.env['ticket'].create(datas)
                    #record.offer_notes = str(datas)
                    #record.request_notes = str(new_ticket)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})

    
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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.id))),('state','=','open'),('action','=','req_cost_select')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)

            # add pending ticket(s) for each requested item's assigned user to request ticket_ids and item ticket_ids
            selected_items = record.request_item_ids.filtered(lambda r: r.state == 'selected')
            if selected_items:
                for item in selected_items:
                    item.state = 'to_confirm'
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing.item', item.id)),
                        'request_costing_id': record.id,
                        'user_id': item.assigned_user_id.id,
                        'action':'req_cost_confirm_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state':'open',
                    }
                    new_ticket = self.env['ticket'].create(datas)
                    #item.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #item.ticket_ids = [(4, new_ticket.id)]
                    #record.ticket_ids = [(4, new_ticket.id)]


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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.id))),('state','=','open')])
            if related_ticket_ids:
                datas = {
                    'state':'cancel',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)

            
            
    


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
                "default_assigned_user_id": self.assigned_user_id.id or self.product_id.buyer_id.id or False,
                },
        }
        return result

    def action_generate_po_mass(self):
        for record in self.request_item_ids.filtered(lambda r: r.type == 'external' and not r.po_id):
            record.generate_po()




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
    
    is_sale_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_team_leader = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_sale_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_team_leader = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_manager = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_purchase_any = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    is_pa_user = fields.Boolean(compute="_compute_is_user", store=False, compute_sudo=True)
    
    @api.onchange('current_user_id')
    @api.depends('current_user_id')
    def _compute_is_user(self):
        for record in self:

            record.is_pa_user = False
            
            record.is_sale_user = False
            record.is_sale_team_user = False
            record.is_sale_team_leader = False
            record.is_sale_manager = False
            record.is_sale_any = False

            record.is_purchase_user = False
            record.is_purchase_team_leader = False
            record.is_purchase_manager = False
            record.is_purchase_any = False

            record.is_pa_user = self.env.user.has_group('ges_logistics_application_partner.group_partner_application_admin') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_team_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_own_docs')

            if record.current_user_id and record.request_id:
                if record.request_id.requester_user_id:
                    record.is_sale_user = record.current_user_id == record.request_id.requester_user_id
            
            if record.current_user_id and record.current_sales_ou_id and record.request_id:
                if record.request_id.sales_ou_id:
                    record.is_sale_team_user = record.current_sales_ou_id == record.request_id.sales_ou_id and (self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_all_docs') or self.env.user.has_group('ges_logistics_application_partner.group_partner_application_user_team_docs'))

            if record.current_user_id and record.current_sales_ou_id and record.request_id:
                if record.request_id.sales_ou_id:
                    if record.request_id.sales_ou_id.requester_user_id:
                        record.is_sale_team_leader = record.current_user_id == record.request_id.sales_ou_id.requester_user_id

            record.is_sale_manager = self.env.user.has_group('sales_team.group_sale_manager')
            record.is_sale_any = record.is_sale_user or record.is_sale_team_user or record.is_sale_team_leader or record.is_sale_manager

            if record.current_user_id and record.assigned_user_id:
                record.is_purchase_user = record.current_user_id == record.assigned_user_id

            if record.current_user_id and record.assigned_user_id:
                if record.assigned_ou_id.requester_user_id:
                    record.is_purchase_team_leader = record.current_user_id == record.assigned_ou_id.requester_user_id 
            
            record.is_purchase_manager = self.env.user.has_group('purchase.group_purchase_manager')
            record.is_purchase_any = record.is_purchase_user or record.is_purchase_team_leader or record.is_purchase_manager
        
        
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
    ticket_ids = fields.One2many('ticket','request_costing_item_id', string="Tickets", auto_join=True)

    @api.depends('vendor_id','product_id','type')
    @api.onchange('vendor_id','product_id','type')
    def _compute_assigned_user_id(self):
        for record in self:
            if record.type == 'external':
                if record.vendor_id and not (record._origin.id and record.assigned_user_id):
                    record.assigned_user_id = record.vendor_id.buyer_id
            elif record.type == 'internal':
                if record.product_id and not (record._origin.id and record.assigned_user_id):
                    record.assigned_user_id = record.product_id.buyer_id

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
        ('confirmed','To Confirm'),
        ('rejected_selection', 'Rejected'), 
        ('to_bill', 'To Bill'),
        ('billed', 'Billed'),
        ('rejected_billing', 'Rejected'),
        ('billed', 'Billed'),
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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_cost_item')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)
            
            # add pending ticket(s) for assigned_ou_id team leaders

            user_ids = record.assigned_ou_id.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_purchase',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].create(datas)
                    #raise UserError(str(new_ticket.id))
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
                    
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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})

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
            
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                        'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'user_id': user.id,                        
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].create(datas)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_cost_item')])
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)
            
            # add pending ticket(s) for assigned_ou_id team leaders

            user_ids = record.assigned_ou_id.requester_user_id.id
            user_records = False
            if user_ids:
                user_records = self.env['res.users'].search([('id','=',user_ids)])
            if user_records:
                for user in user_records:
                    datas = {
                        'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'user_id': user.id,                        
                        'action':'req_cost_validate_purchase',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    new_ticket = self.env['ticket'].create(datas)
                    #record.write({'ticket_ids': [(4, new_ticket.id)]})
                    #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
    
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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)

            pending_items = record.request_id.request_item_ids.filtered(lambda r: r.state not in ['quoted','failed'])
            #pending_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing', record.request_id.id))),('state','=','open'),('action','in',['req_cost_validate_purchase','req_cost_cost_item'])])
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
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            new_ticket = self.env['ticket'].create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})
    
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

            record.state = 'to_validate_failed'
        
            #close current related tickets and add note
            
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                        'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                        'request_costing_id': record.request_id.id,
                        'request_costing_item_id': record.id,
                        'user_id': user.id,                        
                        'action':'req_cost_cost_item',
                        'opened_datetime': fields.Datetime.now(),
                        'state': 'open',
                    }
                    
                    new_ticket = self.env['ticket'].create(datas)

    def _validate_quote(self, note=False):
        for record in self:

            record.state = 'quoted'
        
            #close current related tickets and add note
            
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_validate_purchase')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})


    def mark_selected(self):
        for record in self:
            record.previous_state = record.state
            record.state = 'selected'

    def remove_mark_selected(self):
        for record in self:
            record.state = record.previous_state

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_confirm_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                                'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'user_id': item.assigned_user_id.id,                        
                                'action':'req_cost_bill_item',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
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
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_confirm_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                                'reference_document': ('%s,%s' % ('request.costing.item', record.id)),
                                'request_costing_id': record.request_id.id,
                                'request_costing_item_id': record.id,
                                'user_id': item.assigned_user_id.id,                        
                                'action':'req_cost_bill_item',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
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
                                'user_id': user.id,                        
                                'action':'req_cost_select',
                                'opened_datetime': fields.Datetime.now(),
                                'state': 'open',
                            }
                            
                            new_ticket = self.env['ticket'].create(datas)
                            #record.write({'ticket_ids': [(4, new_ticket.id)]})
                            #record.request_id.write({'ticket_ids': [(4, new_ticket.id)]})

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_bill_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                            'reference_document': ('%s,%s' % ('request.costing.item', item.id)),
                            'request_costing_id': record.id,
                            'user_id': item.assigned_user_id.id,
                            'action':'req_cost_confirm_item',
                            'opened_datetime': fields.Datetime.now(),
                            'state':'open',
                        }
                        new_ticket = self.env['ticket'].create(datas)
                        #item.write({'ticket_ids': [(4, new_ticket.id)]})
                        #record.write({'ticket_ids': [(4, new_ticket.id)]})
                        #item.ticket_ids = [(4, new_ticket.id)]
                        #record.ticket_ids = [(4, new_ticket.id)]

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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open'),('action','=','req_cost_bill_item')])
            
            if related_ticket_ids:
                datas = {
                    'state':'closed',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
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
                            'reference_document': ('%s,%s' % ('request.costing.item', item.id)),
                            'request_costing_id': record.id,
                            'user_id': item.assigned_user_id.id,
                            'action':'req_cost_confirm_item',
                            'opened_datetime': fields.Datetime.now(),
                            'state':'open',
                        }
                        new_ticket = self.env['ticket'].create(datas)
                        #item.write({'ticket_ids': [(4, new_ticket.id)]})
                        #record.write({'ticket_ids': [(4, new_ticket.id)]})
                        #item.ticket_ids = [(4, new_ticket.id)]
                        #record.ticket_ids = [(4, new_ticket.id)]



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
            related_ticket_ids = self.env['ticket'].search([('reference_document','=',('%s,%s' % ('request.costing.item', record.id))),('state','=','open')])
            
            if related_ticket_ids:
                datas = {
                    'state':'cancel',
                    'closed_datetime': fields.Datetime.now(),
                    'note': note,
                }
                related_ticket_ids.write(datas)



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
    can_confirmed = fields.Boolean(compute="_compute_can_confirmed", store=False)
    can_billed = fields.Boolean(compute="_compute_can_billed", store=False)

    can_remove_quoted = fields.Boolean(compute="_compute_can_remove_quoted", store=False)
    can_remove_failed = fields.Boolean(compute="_compute_can_remove_failed", store=False)
    can_remove_suggested = fields.Boolean(compute="_compute_can_remove_suggested", store=False)
    can_remove_required = fields.Boolean(compute="_compute_can_remove_required", store=False)
    can_remove_selected = fields.Boolean(compute="_compute_can_remove_selected", store=False)
    can_remove_confirmed = fields.Boolean(compute="_compute_can_remove_confirmed", store=False)
    can_remove_billed = fields.Boolean(compute="_compute_can_remove_billed", store=False)
    can_remove_billed = fields.Boolean(compute="_compute_can_remove_billed", store=False)

    @api.depends('request_id.state')
    def _compute_can_create(self):
        for record in self:
            record.can_create = False
            if record.request_id.state in ['draft','selection'] and (record.is_sale_any or record.is_purchase_any):                
                record.can_create = True
    
    @api.depends('request_id.state','requested')
    def _compute_can_edit(self):
        for record in self:
            record.can_edit = False
            if record.request_id.state in ['draft'] and record.is_sale_any and record.requested:                
                record.can_edit = True
            if record.request_id.state in ['costing'] and record.is_purchase_any:                
                record.can_edit = True
        
    @api.depends('request_id.state','requested')
    def _compute_can_delete(self):
        for record in self:
            record.can_delete = False
            if record.request_id.state in ['draft'] and record.is_sale_any and record.requested :                
                record.can_delete = True
            if record.request_id.state in ['costing'] and record.is_purchase_any and not record.requested :                
                record.can_delete = True

    @api.depends('request_id.state','state')
    def _compute_can_cancel(self):
        for record in self:
            record.can_cancel = False
            if record.request_id.state not in ['draft'] and record.is_sale_any and not record.state == 'cancel':                
                record.can_cancel = True
            if record.request_id.state in ['costing'] and record.is_purchase_any and not record.state == 'cancel':                
                record.can_cancel = True
    
    @api.depends('request_id.state','type','po_id')
    def _compute_can_generate_po(self):
        for record in self:
            record.can_generate_po = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.type == 'external' and not record.po_id:                
                record.can_generate_po = True

    @api.depends('request_id.state','po_id','type','state')
    def _compute_can_submitted(self):
        for record in self:
            record.can_submitted = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and ((record.type == 'external' and record.po_id) or (record.type == 'internal')) and record.state not in ['quoted','failed','to_validate','to_validate_failed']:
                record.can_submitted = True

    @api.depends('request_id.state','po_id','state')
    def _compute_can_validated(self):
        for record in self:
            record.can_validated = False
            if record.request_id.state in ['costing'] and (record.is_purchase_team_leader or record.is_purchase_manager) and record.state in ['to_validate']:
                record.can_validated = True

    @api.depends('request_id.state','state')
    def _compute_can_failed(self):
        for record in self:
            record.can_failed = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state not in ['quoted','failed','to_validate','to_validate_failed']:
                record.can_failed = True

    @api.depends('request_id.state','po_id','state')
    def _compute_can_validate_failed(self):
        for record in self:
            record.can_validate_failed = False
            if record.request_id.state in ['costing'] and (record.is_purchase_team_leader or record.is_purchase_manager) and record.state == 'to_validate_failed':
                record.can_validate_failed = True


    @api.depends('request_id.state','po_id','type','state')
    def _compute_can_quoted(self):
        for record in self:
            record.can_quoted = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and ((record.type == 'external' and record.po_id) or (record.type == 'internal')) and record.state not in ['quoted','failed','to_validate','to_validate_failed']:
                record.can_quoted = True
    
    @api.depends('request_id.state','state')
    def _compute_can_remove_quoted(self):
        for record in self:
            record.can_remove_quoted = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'quoted':
                record.can_remove_quoted = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_failed(self):
        for record in self:
            record.can_remove_failed = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'failed':
                record.can_remove_failed = True
    
    @api.depends('request_id.state','state')
    def _compute_can_suggested(self):
        for record in self:
            record.can_suggested = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'quoted':
                record.can_suggested = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_suggested(self):
        for record in self:
            record.can_remove_suggested = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'suggested':
                record.can_remove_suggested = True
    
    @api.depends('request_id.state','state')
    def _compute_can_required(self):
        for record in self:
            record.can_required = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'quoted':
                record.can_required = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_required(self):
        for record in self:
            record.can_remove_required = False
            if record.request_id.state in ['costing'] and record.is_purchase_any and record.state == 'required':
                record.can_remove_required = True

    @api.depends('request_id.state','state')
    def _compute_can_selected(self):
        for record in self:
            record.can_selected = False
            if record.request_id.state in ['selection'] and record.is_sale_any and record.state in ['quoted','suggested']:
                record.can_selected = True

    @api.depends('request_id.state','state')
    def _compute_can_remove_selected(self):
        for record in self:
            record.can_remove_selected = False
            if record.request_id.state in ['selection'] and record.is_sale_any and record.state == 'selected':
                record.can_remove_selected = True

    @api.depends('request_id.state','type','po_id.state','state')
    def _compute_can_confirmed(self):
        for record in self:
            record.can_confirmed = False
            if record.request_id.state in ['confirmation'] and record.is_purchase_any and ((record.type == 'external' and record.po_id and record.po_id.state in ['purchase','done']) or (record.type == 'internal')) and record.state == 'to_confirm':
                record.can_confirmed = True

    @api.depends('request_id.state','type','po_id.state','state')
    def _compute_can_remove_confirmed(self):
        for record in self:
            record.can_remove_confirmed = False
            if record.request_id.state in ['confirmation'] and record.is_purchase_any and ((record.type == 'external' and record.po_id and record.po_id.state not in ['purchase','done']) or (record.type == 'internal')) and record.state == 'to_bill':
                record.can_remove_confirmed = True

    @api.depends('request_id.state','type','po_id.state','po_id.invoice_status','state')
    def _compute_can_billed(self):
        for record in self:
            record.can_billed = False
            if record.request_id.state in ['billing'] and record.is_purchase_any and ((record.type == 'external' and record.po_id and record.po_id.invoice_status == 'invoiced') or (record.type == 'internal')) and record.state == 'to_bill':
                record.can_billed = True

    @api.depends('request_id.state','po_id.state','po_id.invoice_status','state')
    def _compute_can_remove_billed(self):
        for record in self:
            record.can_remove_billed = False
            if record.request_id.state in ['billing'] and record.is_purchase_any and ((record.type == 'external' and record.po_id and record.po_id.invoice_status != 'invoiced') or (record.type == 'internal')) and record.state == 'billed':
                record.can_remove_billed = True
    