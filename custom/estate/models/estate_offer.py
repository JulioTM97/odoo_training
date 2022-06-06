from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Offers made to this property"
    _order = "price desc"

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
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)

    _sql_constraints = [
        ('check_price','CHECK (price >= 0)', 'The offer price must be a positive number.')
    ]

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
    
    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model
    #vals es un diccionario que contiene el registro que se esta creando (en este caso)
    def create(self,vals):
        #esto devuelve un objeto
        estate_property = self.env['test.model'].browse(vals['property_id'])
        if estate_property.best_offer > vals['price']:
            raise UserError('You have to improve the offer.')
        estate_property.state = 'offer received'
        return super().create(vals)