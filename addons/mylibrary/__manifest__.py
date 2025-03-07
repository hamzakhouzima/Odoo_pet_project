{
    'name': 'mylibrary',  # Remove the trailing space
    'version': '1.0',
    'sequence': 1,
    'summary': 'Short description of my module',
    'description': 'Long description of my module',
    'category': 'Services',
    'author': 'Hamza',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/book/book_views.xml',    
        'views/book/book_action.xml',
        'views/book/book_menu.xml',
        'views/author/author_views.xml',
        'views/author/author_action.xml',
        'views/author/author_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
