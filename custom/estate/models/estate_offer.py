from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

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
    validity = fields.Integer(default=7, required=True)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            #Si el campo create_date no esta vacio...
            if(record.create_date != False):
                record.date_deadline = relativedelta(days=record.validity) + record.create_date
            else:
                #Campos computados necesitan obligatoriamente un valor (desde la version 13 segun Daniel)
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if(record.date_deadline != False and record.create_date):
                #validity_days debe ser un objeto date
                validity_days = record.date_deadline - record.create_date.date()
                record.validity = validity_days.days
        