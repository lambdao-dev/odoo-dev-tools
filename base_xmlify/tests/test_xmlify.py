# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestXmlify(TransactionCase):
    def test_xmlify(self):
        # TODO: make a test that actually tests something
        user = self.env.ref("base.user_admin")
        node_list = user.xmlify()
        self.assertEqual(len(node_list), 1)
