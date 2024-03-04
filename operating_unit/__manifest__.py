# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License: LGPL-3 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Units",
    "summary": "An operating unit (OU) is an organizational entity part of a "
    "company",
    "version": "17.0.1.0.1",
    "author": "GES Logistics ",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic",
    "depends": [
        "base","mail"
    ],
    "license": "LGPL-3",
    "data": [
        "security/operating_unit_security.xml",
        "security/ir.model.access.csv",
        "data/unit_data.xml",
        "view/operating_unit_view.xml",
        "view/res_users_view.xml",
    ],
}
