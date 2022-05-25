from odoo import fields, models

class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Feature tags for this property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)', "The name of the property must be unique.")
    ]