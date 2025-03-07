from odoo import models , fields

class Author(models.Model):
    _name = "library.author"
    _description = "This model contains the authors' information"

    name = fields.Char(string="Name", required=True)
    birthday = fields.Date(string="Birthday", required=True)
    origin = fields.Char(string="Country", required=True)
    book_ids = fields.One2many('library.book', 'author_id', string="Books")