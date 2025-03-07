from datetime import timedelta
from odoo import models, fields,api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"

    _sql_constraint = [('price_must_be_positive' , 'CHECK(price > 0)')]

    price = fields.Float(required = True)
    partner_id = fields.Many2one("res.partner" , required = True)
    property_id  = fields.Many2one("estate.property" , required =True)
    validity = fields.Integer(default = 7)

    date_deadline = fields.Date(string="Deadline",
    compute="_compute_date_deadline",
    inverse="_inverse_date_deadline"
    ) #compute via validity

    property_type_id = fields.Many2one("estate.property.type")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)


    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days


    @api.onchange('validity')
    def _onchange_validity(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
