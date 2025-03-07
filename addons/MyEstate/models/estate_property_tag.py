from odoo import models,fields,api

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _sql_constraint = [('name_must_be_unique' , 'UNIQUE (name)')]

    name = fields.Char(required=True)
    color = fields.Integer()

