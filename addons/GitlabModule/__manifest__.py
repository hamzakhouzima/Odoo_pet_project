{
    'name': 'kzm_gitlab_integration',
    'version': '1.0',
    'summary': 'Integration with GitLab API for project management',
    'description': """
        This module provides integration with GitLab API to manage client projects,
        including synchronization of branches, pipeline status, and code quality checks.
    """,
    'category': 'Tools',
    'author': 'Your Name or Company',
    'website': 'https://google.com',
    'depends': ['base'],
    'external_dependencies': {
        'python': ['python-gitlab'],
    },        # 'security/ir.model.access.csv',
        # 'security/groups.xml',
    'data': [
        'data/odoo_version_data.xml',
        'views/gitlab_credentials_views.xml',
        'views/gitlab_members_views.xml',
        'views/project_database_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}