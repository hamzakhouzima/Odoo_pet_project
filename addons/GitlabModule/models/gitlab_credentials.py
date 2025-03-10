from odoo import models, fields, api
import gitlab

class GitlabCredentials(models.Model):
    _name = 'gitlab.credentials'
    _description = 'GitLab Credentials'

    username = fields.Char(string="Username", required=True)
    token = fields.Char(string="Token", required=True)
    active = fields.Boolean(string="Active", default=False)



    def action_delete(self):
        for record in self:
            record.unlink()
        return True    



    def action_verify_access(self):
        """Verify GitLab credentials."""
        for record in self:
            try:
                gl = gitlab.Gitlab('https://gitlab.com', private_token=record.token)
                gl.auth()  
                record.active = True
            except Exception as e:
                record.active = False
                raise models.UserError(f"Verification failed: {str(e)}")