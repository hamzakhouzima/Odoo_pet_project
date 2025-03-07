from odoo import fields, models , api


class EstateOffer(models.Model):
    _name = 'estate.offer'
    _description = 'Offers made for the real estate properties'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    type_id =  fields.Many2one(related="property_id.property_type_id") #this is from the 3rd demo of compute 

    @api.onchange("price")
    def _onchange_price(self):
        for record in self:
            if record.price < 0:
                # return {"Warning":{"title": _("Warning"), "message":_("Amount is negative , do you need money ??")}}
                raise Warning(("Amount is negative. Do you need money?"))
    