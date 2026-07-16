{
    'name': "estate",


    'category': 'Teste',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
    ],

  
    'license': 'AGPL-3'
}