from odoo import models, fields

class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'Odoo Version'

    # version = fields.Char(string="Version", required=True)
    version = fields.Selection(
        [('16', '16'), ('17', '17'), ('18', '18')],
        string="Version", required=True, default='16')