from odoo import fields, api, models


class LogisticsPopup(models.TransientModel):
    _name = "logistics.popup"
    _description = "Popup Message"

    name = fields.Char(string="Name")
    message = fields.Html(string="Message")
    