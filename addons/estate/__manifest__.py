{
    "name": "Real Estate",
    "summary": "Tracking real estate properties",
    "sequence": 1,
    "version": "17.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base"],
    "data": [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_offer_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menu.xml',
        'demo/demo.xml',
    ],
    'application': True,
}
