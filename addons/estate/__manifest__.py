{
    "name": "Real Estate",
    "summary": "Tracking real estate properties",
    "sequence": 1,
    "version": "17.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base","web"],
    "data": [
        # 'security/res_groups.xml',
        # 'security/ir.model.access.csv',

        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_offer_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menu.xml',
        'views/dashboard_view.xml'
        # 'views/assets.xml'
        # 'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/js/dashboard.js',
            'estate/static/src/xml/dashboard.xml',
            'estate/static/src/css/dashboard.css',
        ],
    },
    'application': True,
}
