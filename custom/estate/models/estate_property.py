from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, models

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"

    name = fields.Char(string="Title")
    description = fields.Text(copy=False)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= lambda self: date.today() + relativedelta(months=3), string="Availability From")
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north","North"),("south","South"),("east","East"),("west","West")],
        help="The garden orientation",
        default="north"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection = [("new","New"),("offer","Offer"),("received","Received"),("offer received","Offer Accepted"),("sold","Sold"),("canceled","Canceled")],
        help = "Property status",
        default = "new"
    )
    type_id = fields.Many2one("estate.type", string="Type of Property")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user, copy=False)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("property.tag", string="Tags")
    offer_ids = fields.One2many("property.offer","property_id")
