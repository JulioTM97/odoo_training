from odoo import fields, models

class EstateType(models.Model):
    _name = "estate.type"
    _description = "Type of Real Estate"
    _order = "sequence,name"

    name = fields.Char(string="Type of Estate", required=True)
    property_ids = fields.One2many('test.model', 'type_id')
    sequence = fields.Integer('Sequence', default=1)


    _sql_constraints = [
        ('check_name','UNIQUE (name)', "The type of property must be unique.")
    ]