# -*- coding: utf-8 -*-

{
    'name': 'GES Operations',
    'summary': """
        GES Operations
    """,
    'version': '17.0.1.0.0',
    'author': 'GES Logistics',
    'category': 'freight',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['product','uom','sale','sale_management','sale_margin','purchase','fleet','base_fontawesome','account','mail','operating_unit_partner','base_address_extended'],
    "assets": {
        "web.assets_backend": [
                "ges_operations/static/src/css/ges_styles.scss",
        ]
    },
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/sequence_data.xml',
        # Views
        'views/freight_address_views.xml',
        'views/freight_incoterms_views.xml',
        'views/freight_port_views.xml',
        'views/freight_package_views.xml',
        'views/freight_airline_views.xml',
        'views/freight_railway_views.xml',
        'views/freight_vehicle_views.xml',
        'views/freight_vessel_views.xml',
        'views/freight_policy_risk_views.xml',
        'views/shipment_order_views.xml',
        'views/shipment_order_package_views.xml',
        'views/shipment_order_package_item_views.xml',
        'views/shipment_order_route_views.xml',
        'views/shipment_order_service_views.xml',
        'views/inherited_views.xml',
        'wizard/logistics_document_configurator_view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
