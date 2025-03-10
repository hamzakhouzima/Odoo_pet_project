from odoo import fields , api, models

class DashboardData(models.Model):
    _name = "dashboard.data"

    name = fields.Char(required=True)
    value = fields.Integer()

    
    def create_data(self, vals):
        return self.env['dashboard.data'].create(vals)

    def read_data(self):
        return self.env['dashboard.data'].search([]).read(['name', 'value'])

    def update_data(self, record_id, vals):
        record = self.env['dashboard.data'].browse(record_id)
        return record.write(vals)

    def delete_data(self, record_id):
        record = self.env['dashboard.data'].browse(record_id)
        return record.unlink()