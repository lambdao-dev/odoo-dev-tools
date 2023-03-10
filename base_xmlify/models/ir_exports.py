# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrExports(models.Model):
    _inherit = "ir.exports"

    default_xml_export = fields.Boolean(
        string="Default XML export.",
        default=False,
        help="If True this export will be used when exporting records to XML",
    )
