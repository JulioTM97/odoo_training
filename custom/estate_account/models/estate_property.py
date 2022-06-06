from odoo import models, fields
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _inherit = "test.model"

    name = fields.Char(string='Name',required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    price_unit = fields.Float(string='Price', required=True)


    def action_sold(self):
        for record in self:
            invoice = record.env['account.move'].create({
                'name':'Test',
                'partner_id':record.buyer_id,
                'move_type':'out_invoice',
                #with_context crea un diccionario que se envia como parametro a la funcion siguiente (._get_default_journal()
                # al cual luego le saco el valor de la variable id)
                'journal_id':record.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal().id,
                'invoice_line_ids':[(0,0,{"name":record.name,"quantity":1,"price_unit":(record.selling_price*1.06)+100})]})
        return super().action_sold()