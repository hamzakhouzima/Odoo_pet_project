from odoo import fields,models,api
from datetime import timedelta
from dateutil.utils import today

class EstateProperty(models.Model):
    _name = "estate.property"
    _description="My Estate model"
    _sql_constrainsts = [('check_expected_price', 'CHECK(expected_price > 0)', 'The price must be positive.'),
                         ('check_selling_price' , 'CHECK(selling_price >= 0)' , 'The price must be positive or could be 0')
                         ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    # date_availability (Date): Date when the property becomes available (default: 3 months from today, computed via _default_date_availability method).
    date_availability = fields.Date(copy=False,
        default=lambda self: today() + timedelta(days=90),
    )
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(required = True)
    bedrooms = fields.Integer(required=True ,default = 2)
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
    state =   state = fields.Selection([
        ("new", "New"),
        ("received", "Offer received"),
        ("accepted", "Offer accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ], default="new")

    active = fields.Boolean()

    property_type_id = fields.Many2one("estate.property.type")
    offer_ids = fields.One2many('estate.offer', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag')

    validity = fields.Integer(default=7)
    # date_deadline = fields.Date(compute="_compute_date_deadline" , inverse="_inverse_deadline")

    is_sold = fields.Boolean(compute="_compute_is_sold" , string="Sold")
    # buyer_id = fields.Many2one("res.users")

    @api.depends("date_availability")
    def _default_date_availability(self):
        for att in self:
            att.date_availability = today() + timedelta(days=90)

    # @api.onchange('garden')
    # def onchange_garden_area(self):
    #     for att in self:
    #         att.garden_area = 0
    #         att.garden_orientation = False

    def action_sold(self):
        for att in self:
            if att.state not in ('canceled', 'sold'):
                att.state = 'sold'
                att.selling_price = max(att.offer_ids.mapped('price'))
            else:
                raise Warning(("Already sold or canceled"))

    def action_cancel(self):
        for att in self:
            if att.state not in ('canceled' , 'sold'):
                att.state = 'canceled'

    def accept_offer(self):
        for att in self:
            att.status = 'accepted'  # Update this offer's status
            att.property_id.state = 'offer_accepted'
