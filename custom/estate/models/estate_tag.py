from odoo import fields, models

class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Feature tags for this property"

    name = fields.Char(required=True)