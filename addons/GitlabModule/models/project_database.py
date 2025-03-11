from odoo import models, fields, api
import gitlab
import subprocess
from odoo.exceptions import UserError
import logging
import re  

class ProjectDatabase(models.Model):
    _name = 'project.database'
    _description = 'Project Database'
    _logger = logging.getLogger(__name__)

    name = fields.Char(string="Name", required=True)
    client = fields.Many2one('res.partner', string="Client")
    link = fields.Char(string="Link")
    version = fields.Many2one('odoo.version', string="Odoo Version" , required=True, default=lambda self: self.env['odoo.version'].search([('version', '=', '16')], limit=1).id)
    git_link = fields.Char(string="Git Link")
    position = fields.Selection([('prod', 'PROD'), ('test', 'TEST'), ('pre_prod', 'Pré-PROD')], string="Position")
    branch_count = fields.Integer(string="Number of Branches", readonly=True)
    group = fields.Char(string="Group")
    project_name = fields.Char(string="Project Name")
    default_branch = fields.Char(string="Default Branch", readonly=True)
    pipeline_status = fields.Selection([('succeed', 'Succeed'), ('failed', 'Failed')], string="Pipeline Status")
    project_members = fields.Many2many('projet.members', string="Project Members", readonly=True)
    code_quality = fields.Float(string="Code Quality / 10", readonly=True)
    last_merge_request = fields.Char(string="Last Merge Request")
    access_token_id = fields.Many2one('gitlab.credentials', string="Access Token")

    def action_synchronize(self):
        """Synchronize data with GitLab."""
        for record in self:
            if not record.access_token_id:
                raise UserError("No GitLab credentials provided.")

            if not record.git_link:
                raise UserError("GitLab project link not provided.")

            try:
                # Initialize GitLab API client
                gl = gitlab.Gitlab('https://gitlab.com', private_token=record.access_token_id.token)
                gl.auth()  # Ensure authentication is valid
                
                # Extract project path correctly from the git_link
                project_path = self._extract_project_path(record.git_link)
                
                self._logger.info(f"Fetching project: {project_path}")
                
                # Get the project from GitLab
                project = gl.projects.get(project_path)
                
                # Sync the project data
                self._sync_project_data(record, project)
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success',
                        'message': f'Project "{record.name}" synchronized successfully.',
                        'type': 'success',
                    }
                }

            except gitlab.exceptions.GitlabAuthenticationError as e:
                self._logger.error(f"Authentication error for '{record.git_link}': {e}")
                raise UserError("Invalid GitLab token. Please check your credentials.")
            except gitlab.exceptions.GitlabGetError as e:
                self._logger.error(f"Error fetching project '{record.git_link}': {e}")
                if hasattr(e, 'response_body'):
                    self._logger.error(f"Response Body: {e.response_body}")
                raise UserError(f"Could not fetch project: {e}")
            except Exception as e:
                self._logger.exception(f"Unexpected error for '{record.git_link}': {e}")
                raise UserError(f"An unexpected error occurred: {e}")

    def _extract_project_path(self, git_link):
        """Extract the project path from a GitLab URL or return as is if already in the right format."""
        if not git_link:
            return ""
            
        # If it's a URL with gitlab.com in it
        if 'gitlab.com' in git_link:
            # Clean up URL and extract the project path
            gitlab_url_regex = r'gitlab\.com/(.+?)(?:\.git)?/?$'
            match = re.search(gitlab_url_regex, git_link)
            if match:
                return match.group(1)
            else:
                # Fallback to simple splitting
                return git_link.strip('/').split('gitlab.com/')[-1]
                
        # Already in group/project format or ID
        return git_link.strip('/')

    def _sync_project_data(self, record, project):
        """Synchronize the project-related fields."""
        try:
            # Update basic project information
            record.write({
                'project_name': project.name,
                'group': project.namespace['full_path'],
                'default_branch': project.default_branch,
            })
            
            # Get branches
            try:
                branches = project.branches.list(all=True)
                record.branch_count = len(branches)
            except Exception as e:
                self._logger.warning(f"Error fetching branches: {e}")
                record.branch_count = 0
            
            # Get project members
            try:
                members = project.members.list(all=True)
                # Clear existing members and add new ones
                member_vals = []
                for member in members:
                    # Check if member already exists
                    existing_member = self.env['projet.members'].search([('name', '=', member.name)])
                    if existing_member:
                        member_vals.append((4, existing_member.id))
                    else:
                        # Create new member
                        new_member = self.env['projet.members'].create({'name': member.name})
                        member_vals.append((4, new_member.id))
                
                record.project_members = [(5, 0, 0)] + member_vals
            except Exception as e:
                self._logger.warning(f"Error fetching members: {e}")
            
            # Get merge requests
            try:
                merged_mrs = project.mergerequests.list(state='merged', order_by='updated_at', sort='desc')
                record.last_merge_request = merged_mrs[0].title if merged_mrs else 'No merge requests'
            except Exception as e:
                self._logger.warning(f"Error fetching merge requests: {e}")
                record.last_merge_request = 'Error fetching merge requests'
            
            # Get pipeline status
            try:
                pipelines = project.pipelines.list(ref=record.default_branch)
                record.pipeline_status = 'succeed' if pipelines and pipelines[0].status == 'success' else 'failed'
            except Exception as e:
                self._logger.warning(f"Error fetching pipelines: {e}")
                record.pipeline_status = 'failed'
                
        except gitlab.exceptions.GitlabError as e:
            self._logger.error(f"Error syncing data for project '{project.name}': {e}")
            raise UserError(f"Error syncing project data: {e}")

    def action_code_quality(self):
        """Run pylint and assign code quality score."""
        for record in self:
            if not record.git_link:
                raise UserError("GitLab project link not provided.")
                
            try:
                # Need to clone the repository first before analyzing
                # This is a simplified example - in production, you'd want to
                # clone the repo to a temporary directory and analyze it there
                
                # Use the git_link as path for pylint (assuming it's a local path after cloning)
                # In a real scenario, you would:
                # 1. Clone the repo using GitPython or subprocess
                # 2. Run pylint on the local files
                cmd = f"pylint --load-plugins=pylint_odoo --fail-under=7.00 --max-line-length=130 --disable=F0401,R0801,R1720,W0212,R1725,W0201,C8101,E0611,R0903,C0116 {record.git_link}"
                
                self._logger.info(f"Running pylint: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode in [0, 32]:  # pylint return codes for success or warnings
                    # Extract score from pylint output
                    score_text = result.stdout.split('Your code has been rated at ')
                    if len(score_text) > 1:
                        score = float(score_text[1].split('/10')[0])
                        record.code_quality = score
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Code Quality',
                                'message': f'Code quality: {score}/10',
                                'type': 'success',
                            }
                        }
                    else:
                        raise UserError("Could not parse pylint output")
                else:
                    self._logger.error(f"Pylint error: {result.stderr}")
                    raise UserError(f"Pylint error: {result.stderr}")
                    
            except Exception as e:
                self._logger.exception(f"Error analyzing code quality: {e}")
                raise UserError(f"Error analyzing code quality: {e}")