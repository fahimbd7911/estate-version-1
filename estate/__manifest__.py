{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Fahim",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data':[
        'security/ir.model.access.csv',
        'views/inherit_view.xml',
        'views/estate_property_views.xml',
        'views/property_tag_view.xml',
        'views/property_type_views.xml',
        'views/offer_view.xml',
        'views/estate_menus.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False
}
