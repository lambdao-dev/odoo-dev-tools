# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestCreateViews(TransactionCase):
    def test_primary_views(self):
        model = self.env["ir.model"].search([("model", "=", "view.export.wizard")])
        vals = {"model_id": model.id, "destination": "/tmp/"}
        wizard = self.env["view.export.wizard"].create(vals)
        wizard.viewify()
        # TODO
        self.assertTrue(True)

    def test_inherited_view(self):
        model = self.env["ir.model"].search([("model", "=", "res.partner")])
        module = self.env["ir.module.module"].search([("name", "=", "web")])
        vals = {"model_id": model.id, "destination": "/tmp/", "module_id": module.id}
        wizard = self.env["view.export.wizard"].create(vals)
        wizard.viewify()
        # TODO
        self.assertTrue(True)
