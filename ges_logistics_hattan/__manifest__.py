# -*- coding: utf-8 -*-

{
    'name': 'GES Logistics',
    'summary': """
        GES Logistics
    """,
    'version': '17.0.1.0.0',
    'author': 'GES Logistics',
    'category': 'freight',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['product', 'sale','sale_management','crm','purchase','base_fontawesome','fleet','base_address_extended'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/logistics_sequence_data.xml',
        # Views
        'views/inherited_views.xml',
        'views/logistics_configurations.xml',
        'views/logistics_shipment_order_view.xml',
        'views/logistics_transport_order_view.xml',
        'views/logistics_storage_order_view.xml',
        'views/logistics_customs_order_view.xml',
        'views/logistics_service_order_view.xml',
        'views/menu.xml',
        'wizard/logistics_popup_view.xml',
        'wizard/logistics_document_configurator_view.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
