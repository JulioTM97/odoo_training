from ast import Pass
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

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
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    
    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
            for record in self:
                record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
            for record in self:
                record.best_offer = max(record.offer_ids.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled.")
            else:
                record.state = "canceled"
        return True