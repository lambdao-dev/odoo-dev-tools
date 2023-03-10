# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Base module to generate Odoo views",
    "summary": "Base module to generate Odoo views",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "website": "https://github.com/lambdao-dev/odoo-dev-tools",
    "author": "len-foss",
    "license": "AGPL-3",
    "installable": True,
    "auto-install": True,
    "depends": ["mail"],  # could be reduced to base if needed
    "data": [
        "wizard/view_export_wizard_view.xml",
        "security/view_export_wizard.xml",
    ],
}
