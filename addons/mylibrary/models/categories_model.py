from odoo import models, fields 


class CategoryModel(models.Model):
    _name = 'library.Category'
    _description = 'Library Category'
    category = fields.Char(string="Category", required=True)
    book_ids = fields.One2many('category', 'inverse_field_name', string='field_name')
