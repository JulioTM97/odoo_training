from odoo import fields, models

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Offers made to this property"

    price = fields.Float()
    status = fields.Selection(
        selection = [("accepted","Accepted"),("refused","Refused")],
        help = "Offer status",
        copy = False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("test.model", required=True)
    