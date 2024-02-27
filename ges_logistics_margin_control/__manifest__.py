# -*- coding: utf-8 -*-

{
    'name': 'GES Margin Control',
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
    'depends': ['ges_logistics_application_partner','sale_margin'],
    
    'data': [
        
        #views
        'views/sale_order.xml',
      
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
