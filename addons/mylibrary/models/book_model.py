from odoo import models, fields

class BookModel(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    name = fields.Char(string="Title", required=True)
    # author = fields.Char(string="Author")
    published_date = fields.Date(string="Published Date")
    isbn = fields.Char(string="ISBN")
    copies_available = fields.Integer(string="Copies Available", default=1)
    author_id = fields.Many2one("library.author", string="Author")
    category_id = fields.Many2one("library.category" , string="Category")