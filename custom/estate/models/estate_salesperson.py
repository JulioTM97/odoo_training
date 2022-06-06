from odoo import fields, models

class Salesperson(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('test.model','salesman_id')