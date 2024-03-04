# -*- coding: utf-8 -*-

{
    'name': 'GES Logistics Faizal',
    'summary': """
        GES Logistics
    """,
    'version': '17.2.1',
    'author': 'GES Logistics',
    'category': 'freight',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['crm', 'product', 'sale_management', 'sale', 'fleet'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/logistics_sequence_data.xml',
        # Views
        'views/inherited_views.xml',
        'views/payment_request.xml',
        'views/logistics_configurations.xml',
        'views/logistics_shipment_order_view.xml',
        'views/logistics_transport_order_view.xml',
        'views/logistics_storage_order_view.xml',
        'views/logistics_customs_order_view.xml',
        'views/logistics_service_order_view.xml',
        'views/menu.xml',
        # Reports
        'reports/terminal_transport_waybill.xml',
        'reports/transport_order_report_view.xml',

    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
