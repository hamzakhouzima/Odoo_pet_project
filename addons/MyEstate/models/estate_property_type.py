from odoo import models, fields , api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _sql_constraint = [("check_if_unique" , "UNIQUE(name)")]

    name = fields.Char(required=True)
    sequence = fields.Integer(defaul=10)
    property_ids = fields.One2many("estate.property" , "property_type_id")
    offer_count = fields.Integer() #add a compute after finishing the fields
    offer_ids = fields.Many2many("estate.offer" , compute="_compute_offer")#add a compute via _compute_offer

    @api.depends("offer_count")
    def _compute_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids.filtered(lambda o: o.state != 'canceled'))

    