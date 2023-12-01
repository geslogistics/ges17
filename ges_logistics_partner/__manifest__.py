# -*- coding: utf-8 -*-

{
    'name': 'GES Partner',
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
    'depends': ['base','base_automation','sale','sale_management','crm','purchase','account'],
    'assets': {
        'web.assets_backend': [
            'ges_logistics_partner/static/src/css/pa_styles.css',
        ],
    },
    'data': [
        # Data
        'data/application_sequence_data.xml',
        'data/automated_actions.xml',
        'data/purchase_team_data.xml',

        #security
        'security/customer_supplier_approval_groups.xml',
        'security/ir.model.access.csv',
        
        #views
        'views/purchase_team_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_application_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/crm_views.xml',

        #wizard
        'wizard/res_application_action_wizard_views.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
