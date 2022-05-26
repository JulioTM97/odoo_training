from odoo import fields, models,api

class EstateType(models.Model):
    _name = "estate.type"
    _description = "Type of Real Estate"
    _order = "sequence,name"

    name = fields.Char(string="Type of Estate", required=True)
    property_ids = fields.One2many('test.model', 'type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_search_offers")

    _sql_constraints = [
        ('check_name','UNIQUE (name)', "The type of property must be unique.")
    ]

    @api.depends("offer_count")
    def _compute_search_offers(self):
        for record in self:
            record.offer_count = len(record.mapped('offer_ids') if type(record.mapped('offer_ids')!=int) else 0)