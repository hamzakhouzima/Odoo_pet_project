from odoo import models, fields

class ProjectMembers(models.Model):
    _name = 'projet.members'
    _description = 'Project Members'

    name = fields.Char(string="Name", required=True)