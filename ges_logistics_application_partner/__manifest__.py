# -*- coding: utf-8 -*-

{
    'name': 'GES Application Partner',
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
    'depends': ['base','mail','l10n_sa','l10n_sa_edi','base_automation','sale','sale_management','crm','crm_checklist','purchase','account','ges_logistics_application_base','ges_logistics_ticket','ges_logistics','operating_unit_partner','operating_unit_product'],
    'assets': {
        'web.assets_backend': [
            'ges_logistics_application_partner/static/src/css/pa_styles.css',
        ],
    },
    'data': [
        # Data
        'data/application_sequence_data.xml',
        'data/automated_actions.xml',

        #security
        'security/security_config.xml',
        'security/ir.model.access.csv',
        
        #views
        'views/res_partner_views.xml',
        'views/application_partner_views.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',

        #wizard
        'wizard/res_application_action_wizard_views.xml',
        'wizard/application_action_wizard_views.xml',

        #report
        'wizard/res_application_action_wizard_views.xml',
        'report/sale_report.xml',
        'report/purchase_report.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
