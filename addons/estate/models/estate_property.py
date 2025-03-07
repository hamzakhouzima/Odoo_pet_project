from datetime import timedelta
from dateutil.utils import today
from odoo import models, fields,api
# from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "sequence desc"

    sequence = fields.Integer(default=1)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: today() + timedelta(days=90),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    # selling_price = fields.Float(compute="_compute_is_sold")

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("new", "New"),
        ("received", "Offer received"),
        ("accepted", "Offer accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ], default="new")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    property_type_id = fields.Many2one('estate.property.type')
    offer_ids = fields.One2many('estate.offer', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag')

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline" , inverse="_inverse_deadline")

    is_sold = fields.Boolean(compute="_compute_is_sold" , string="Sold")


    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area

    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_price = 0

    def _inverse_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline   - fields.Date.today).days

    

    #this is to make the set sold or not value 
    @api.depends("selling_price")
    def _compute_is_sold(self):
        for rec in self:
            rec.is_sold = rec.selling_price > 0




    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            rec.garden_area = 0 if not rec.garden else rec.garden_area or 0

                
    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for rec in self:
            if rec.date_availability and rec.date_availability < fields.Date.today():
                raise Warning(("The availability date is in the past."))

              
    
    def sell_estate(self):
        for rec in self:
            if rec.state == 'canceled':
                raise Warning(("Cannot sell a canceled property."))
            if rec.offer_ids:
                rec.selling_price = max(rec.offer_ids.mapped('price'))
                rec.state = 'sold'
            else:
                raise Warning(("Cannot sell a property with no offers."))

    def cancel_offer(self):
        for rec in self:
            if rec.state == 'sold':
                raise Warning(("Cannot cancel a property that is already sold."))
            rec.state = 'canceled'


    # def order_by_name(self):
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'estate.property',
    #             'view_mode': 'tree,form',
    #             'views': [(self.env.ref('estate.estate_property_list_view').id, 'tree'), (False, 'form')],
    #             'context': {'order_by': 'name ASC'},
    #             'target': 'current',
    #         }


    # @api.onchange('name')
    # def _onchange_name(self):
    #     for rec in self:
    #         if rec.name:
    #             raise Warning(('File "/mnt/extra-addons/estate/models/estate_offer.py", line 43, in estate_offer'))