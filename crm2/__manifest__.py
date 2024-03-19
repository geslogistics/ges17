# -*- coding: utf-8 -*-

{
    'name': 'GES CRM II',
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
    'depends': ['ges_logistics_application_partner','crm'],
    'assets': {
        'web.assets_backend': [
            'ges_logistics_application_partner/static/src/css/pa_styles.css',
        ],
    },
    'data': [
        

        
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/menu.xml',
    ],
   
    
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
