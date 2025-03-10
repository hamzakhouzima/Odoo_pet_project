from odoo import http
from odoo.http import request

class DashboardController(http.Controller):
    @http.route('/dashboard/data', auth='user', type='json')
    def get_data(self):
        return request.env['dashboard.data'].read_data()

    @http.route('/dashboard/create', auth='user', type='json')
    def create(self, **kwargs):
        return request.env['dashboard.data'].create_data(kwargs)

    @http.route('/dashboard/update', auth='user', type='json')
    def update(self, id, vals):
        return request.env['dashboard.data'].update_data(id, vals)

    @http.route('/dashboard/delete', auth='user', type='json')
    def delete(self, id):
        return request.env['dashboard.data'].delete_data(id)