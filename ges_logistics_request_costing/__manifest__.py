# -*- coding: utf-8 -*-

{
    'name': 'GES Request Costing',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'module_type': 'official',
    'summary': """This module allows users to validate or approve contacts """,
    'description': """By this module, you can grant access to users to validate
                      or approve partners. Then you will be able to select only
                      approved partners on sales orders, purchase orders, 
                      invoices, bills or delivery orders.""",
    'author': 'GES Logistics',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['ges_logistics_request_base','uom','operating_unit'],
    "assets": {
        "web.assets_backend": [
                "ges_logistics_request_costing/static/src/css/ges_styles.scss",
        ]
    },
    'data': [
        # Security
        'security/security_config.xml',
        'security/ir.model.access.csv',
        #data
        'data/logistics_sequence_data.xml',
        #views
        'views/request_costing_view.xml',
        'views/inherited_views.xml',
        'views/menu.xml',
        #wizard
        'wizard/user_action_wizard_views.xml',
        'wizard/request_costing_wizard_views.xml',
      
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
