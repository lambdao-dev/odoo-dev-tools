# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Base Ir Exports",
    "summary": "Module providing a wizard to create exports and views on ir.exports",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "website": "https://github.com/lambdao-dev/odoo-dev-tools",
    "author": "len-foss,Lambdao",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base"],
    "data": [
        "wizard/ir_exports_wizard.xml",
        "views/ir_exports_view.xml",
        "security/ir_exports_wizard.xml",
    ],
    "demo": [],
}
