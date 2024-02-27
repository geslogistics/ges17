# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Units in Partners",
    "summary": "Adds the concept of operating unit (OU) in Partner and Country",
    "version": "17.0.1.0.0",
    "author": "brain-tec AG, "
    "Open Source Integrators, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Product",
    "depends": ["base", "operating_unit"],
    "license": "LGPL-3",
    "data": [
        "security/security.xml",
        "views/partner_view.xml",
        "views/country_view.xml",
    ],
}
