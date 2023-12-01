# -*- coding: utf-8 -*-

{
    'name': 'GES CRM Check List',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'module_type': 'official',
    'author': 'GES Logistics',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['crm'],
    "assets": {
        "web.assets_backend": [
                "crm_checklist/static/src/components/crm_checklist/*.js",
                "crm_checklist/static/src/components/crm_checklist/*.xml",
                "crm_checklist/static/src/components/crm_checklist/*.scss",
                "crm_checklist/static/src/views/**/*.js",
                "crm_checklist/static/src/views/**/*.xml"
        ]
    },
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/crm_stage.xml",
        "views/crm_lead.xml",
        "views/crm_chek_list.xml",
    ],
    
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}




