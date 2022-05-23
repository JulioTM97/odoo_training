from odoo import fields, models

class EstateType(models.Model):
    _name = "estate.type"
    _description = "Type of Real Estate"

    name = fields.Char(string="Type of Estate", required=True)