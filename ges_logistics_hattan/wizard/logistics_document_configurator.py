from odoo import fields, api, models
from odoo.exceptions import ValidationError, UserError


class LogisticsDocConfig(models.TransientModel):
    _name = "logistics.wizard.doc.config"
    _description = "Document Configurator Wizard"

    name = fields.Char(string="Name")
    sol_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    so_id = fields.Many2one('sale.order', string="Sale Order", related="sol_id.order_id")
    product_id = fields.Many2one('product.product', string="Product", related="sol_id.product_id")
    sale_order_line_workflow = fields.Selection([('sho','Shipment Order'),('tro','Transport Order'),('sto','Storage Order'),('cco','Customs Order'),('svo','Service Order')], string="Doc Type", related="product_id.sale_order_line_workflow")
    partner_id = fields.Many2one('res.partner', string="Customer", related="sol_id.order_partner_id")

    shipment_order_id = fields.Many2one('logistics.shipment.order', string="Shipment Order", domain="[('partner_id','=',partner_id)]")
    transport_order_id = fields.Many2one('logistics.transport.order', string="Transport Order", domain="[('partner_id','=',partner_id)]")
    storage_order_id = fields.Many2one('logistics.storage.order', string="Storage Order", domain="[('partner_id','=',partner_id)]")
    customs_order_id = fields.Many2one('logistics.customs.order', string="Customs Order", domain="[('partner_id','=',partner_id)]")
    service_order_id = fields.Many2one('logistics.service.order', string="Service Order", domain="[('partner_id','=',partner_id)]")


    def apply_doc_config_wizard(self):
        if self.sale_order_line_workflow == "sho":
            if self.shipment_order_id:
                self.sol_id.reference_document = '%s,%s' % ('logistics.shipment.order',self.shipment_order_id.id)
                self.sol_id.name = self.sol_id.name + "\n" + "Shipment Desc 1"
            else:
                raise UserError("Select an existing Shipment Order or Create New")
        elif self.sale_order_line_workflow == "tro":
            if self.transport_order_id:
                self.sol_id.reference_document = '%s,%s' % ('logistics.transport.order',self.transport_order_id.id)
                self.sol_id.name = self.sol_id.name + "\n" + "Transportation Desc 1"
            else:
                raise UserError("Select an existing Transport Order or Create New")
        elif self.sale_order_line_workflow == "sto":
            if self.storage_order_id:
                self.sol_id.reference_document = '%s,%s' % ('logistics.storage.order',self.storage_order_id.id)
                self.sol_id.name = self.sol_id.name + "\n" + "Storage Desc 1"
            else:
                raise UserError("Select an existing Storage Order or Create New")
        elif self.sale_order_line_workflow == "cco":
            if self.customs_order_id:
                self.sol_id.reference_document = '%s,%s' % ('logistics.customs.order',self.customs_order_id.id)
                self.sol_id.name = self.sol_id.name + "\n" + "Customs Desc 1"
            else:
                raise UserError("Select an existing Customs Order or Create New")
        elif self.sale_order_line_workflow == "svo":
            if self.service_order_id:
                self.sol_id.reference_document = '%s,%s' % ('logistics.service.order',self.service_order_id.id)
                self.sol_id.name = self.sol_id.name + "\n" + "Service Desc 1"
            else:
                raise UserError("Select an existing Service Order or Create New")
        else:
            raise UserError("Error, No Reference Type")
    
    def action_create_order(self):
        if self.sale_order_line_workflow == "sho":
            model = "logistics.shipment.order"
        elif self.sale_order_line_workflow == "tro":
            model = "logistics.transport.order"
        elif self.sale_order_line_workflow == "sto":
            model = "logistics.storage.order"
        elif self.sale_order_line_workflow == "cco":
            model = "logistics.customs.order"
        elif self.sale_order_line_workflow == "svo":
            model = "logistics.service.order"
        else:
            raise UserError("Error, No Reference Type")

        result = {
            "type": "ir.actions.act_window",
            "res_model": model,
            "view_mode": "form",
            "context": {"default_source_sol_id": self.sol_id.id, "default_partner_id" : self.partner_id.id},
        }
        return result
    
    