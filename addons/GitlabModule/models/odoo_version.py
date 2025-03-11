from odoo import models, fields

class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'Odoo Version'
    _rec_name = 'version'
    # version = fields.Char(string="Version", required=True)
    version = fields.Selection(
    [('16', 'Version 16'), ('17', 'Version 17'), ('18', 'Version 18')],
    string="Version",
    required=True,
    default='16'
    )