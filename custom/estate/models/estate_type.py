from odoo import fields, models

class EstateType(models.Model):
    _name = "estate.type"
    _description = "Type of Real Estate"

    name = fields.Char(string="Type of Estate", required=True)

    _sql_constraints = [
        ('check_name','UNIQUE (name)', "The type of property must be unique.")
    ]