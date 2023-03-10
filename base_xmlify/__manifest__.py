# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Base xmlify",
    "summary": "Base module that provide an xmlify method on all models",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "website": "https://github.com/lambdao-dev/odoo-dev-tools",
    "author": "len-foss",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_ir_export"],
    "external_dependencies": {"python": ["python-slugify"]},
    "data": [
        "views/ir_exports_view.xml",
        "wizard/xml_exports_view.xml",
        "security/xml_exports.xml",
    ],
}
