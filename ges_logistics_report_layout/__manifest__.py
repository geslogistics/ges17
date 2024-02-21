# -*- coding: utf-8 -*-

{
    'name': 'GES Logistics Reports and Layouts',
    'summary': """
        GES Logistics
    """,
    'version': '17.0.1.0.0',
    'author': 'GES Logistics',
    'category': 'freight',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': [],
    'assets': {
        'web.report_assets_common': [
            'ges_logistics_report_layout/static/src/css/base_report_styles.scss',
            'ges_logistics_report_layout/static/src/css/report_styles.scss',
        ],
        'web.assets_backend': [
            'ges_logistics_report_layout/static/src/css/report_styles.scss',
        ],
    },
    'data': [
        # Report
        'report/ges_external_layout.xml',
        'report/ir_actions_report.xml',
        'report/ges_report_saleorder.xml',
        'report/ges_report_purchaseorder.xml',
        'report/ges_report_invoice.xml',
        'report/ges_report_payment_receipt.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
