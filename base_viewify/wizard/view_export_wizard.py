# Copyright 2023 len-foss/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

from lxml import etree
from lxml.builder import E

from odoo import api, fields, models

ignore_fields = ["self", "__last_update", "display_name"]


class ViewExportWizard(models.TransientModel):
    _name = "view.export.wizard"
    _description = "Export to View"

    model_id = fields.Many2one(string="Model", comodel_name="ir.model")
    model_name = fields.Char("Model Name", related="model_id.model", readonly=True)
    filename = fields.Char(string="File name")
    form = fields.Boolean(default=True)
    tree = fields.Boolean(default=True)
    search_view = fields.Boolean(default=True)
    force_primary = fields.Boolean(default=False)
    is_inherit = fields.Boolean(compute="_compute_is_inherit")
    parent_menu = fields.Many2one(comodel_name="ir.ui.menu")
    parent_form_view = fields.Many2one(comodel_name="ir.ui.view")
    parent_tree_view = fields.Many2one(comodel_name="ir.ui.view")
    destination = fields.Char(string="Path to export the file to")
    module_id = fields.Many2one(
        comodel_name="ir.module.module",
        help="If selected, exports only fields defined in that module or "
        "its dependencies.",
    )

    @api.depends("force_primary", "module_id")
    def _compute_is_inherit(self):
        for rec in self:
            rec.is_inherit = self.module_id and not self.force_primary

    def _add_view_to_root(self, root, view_mode):
        root.append(self._get_view_xml(view_mode=view_mode))

    def viewify(self):
        self.ensure_one()
        filename = self.filename or f'{self.model_name.replace(".", "_")}_view.xml'
        destination = self.destination or os.getcwd()
        root = E.odoo()
        if self.form or not self.is_inherit:
            self._add_view_to_root(root, "form")
        if self.tree:
            self._add_view_to_root(root, "tree")
        if self.search_view and not self.is_inherit:
            self._add_view_to_root(root, "search")
        if not self.is_inherit:
            action = self._get_action_xml()
            root.append(action)
            menu = self._get_menu_xml()
            root.append(menu)
        content = etree.tostring(root, encoding="unicode", pretty_print=True)
        with open(os.path.join(destination, filename), "w") as output:
            output.write(content)
        return True

    def _get_fields(self):
        self.ensure_one()
        fs = [
            f
            for f in self.env[self.model_name]._fields.values()
            if f.name not in models.MAGIC_COLUMNS
            and f.name not in ignore_fields
            and f._module not in ("portal", "mail", "sms")
        ]
        if self.module_id:
            fs = [f for f in fs if f._module == self.module_id.name]
        return fs

    def _get_view_id(self, view_mode):
        self.ensure_one()
        return f"view_{view_mode}_{self.model_name.replace('.', '_')}"

    def _get_action_id(self):
        self.ensure_one()
        return f"window_action_{self.model_name.replace('.', '_')}"

    def _get_action_xml(self):
        self.ensure_one()
        xml_id = self._get_action_id()
        action = E.record(model="ir.actions.act_window", id=xml_id)
        action.append(E.field(self.model_name, name="res_model"))
        action.append(E.field(self.model_id.name, name="name"))
        view_modes = [vm for vm in ("tree", "form") if self[vm]]
        action.append(E.field(",".join(view_modes), name="view_mode"))
        # TODO: add view ref?
        # action.append(E.field(name="view_id", ref=self._get_view_id("form")))
        target = "new" if self.model_id.transient else "current"  # wizards
        action.append(E.field(target, name="target"))
        return action

    def _get_menu_xml(self):
        self.ensure_one()
        menu = E(
            "menuitem",
            id=f"menu_{self.model_name.replace('.', '_')}",
            action=self._get_action_id(),
            name=self.model_id.name,
        )
        parent_menu = self.parent_menu or self.env.ref("base.next_id_9")
        menu.attrib["parent"] = parent_menu.get_external_id()[parent_menu.id]
        return menu

    def _get_default_parent_view(self, view_mode):
        self.ensure_one()
        domain = [
            ("model", "=", self.model_name),
            ("type", "=", view_mode),
            ("inherit_id", "=", False),
        ]
        return self.env["ir.ui.view"].search(domain, limit=1)

    def _get_parent_view(self, view_mode):
        self.ensure_one()
        parent_view = None
        if view_mode == "tree":
            parent_view = self.parent_tree_view
        elif view_mode == "form":
            parent_view = self.parent_form_view
        parent_view = parent_view or self._get_default_parent_view(view_mode)
        return parent_view

    def _get_xpath(self, view):
        try:
            root = etree.fromstring(view.arch)
            f_name = root.xpath("//field")[-1].attrib["name"]
            xpath = f"//field[@name='{f_name}']"
        except Exception:
            xpath = "//TODO"
        return xpath

    def _get_view_xml(self, view_mode="form"):
        self.ensure_one()
        fs = self._get_fields()
        xml_id = self._get_view_id(view_mode)
        view = E.record(model="ir.ui.view", id=xml_id)
        view.append(E.field(self.model_name, name="model"))
        name = ".".join([self.model_name, view_mode])
        view.append(E.field(name, name="name"))
        arch_field = E.field(name="arch", type="xml")
        view.append(arch_field)

        # setup arch field depending on inheritance status
        if self.is_inherit:
            parent_view = self._get_parent_view(view_mode)
            inherit_id = parent_view.get_external_id().get(parent_view.id, "TODO")
            view.append(E.field(name="inherit_id", ref=inherit_id))
            xpath = self._get_xpath(parent_view)
            arch = E.xpath(expr=xpath, position="after")
        else:
            arch = E(view_mode, string=self.model_id.name)
        arch_field.append(arch)

        if not self.is_inherit and self.search_view and view_mode == "tree":
            search_ref = self._get_view_id("search")
            arch.append(E.field(name="search_view_id", ref=search_ref))
        if not self.is_inherit and view_mode == "form":
            if not self.model_id.transient:
                arch.append(E.header())
            sheet = E.sheet()
            if not self.model_id.transient:
                sheet.append(E.div(name="button_box", **{"class": "oe_button_box"}))
            div_name = E.div(**{"class": "oe_title"})
            sheet.append(div_name)
            name_field = "display_name"
            if "name" in [f.name for f in fs]:
                name_field = "name"
                fs.remove(self.env[self.model_name]._fields["name"])
            div_name.append(E.label(**{"for": name_field}))
            div_name.append(E.field(name=name_field))
            arch.append(sheet)
            notebook = E.notebook()
            sheet.append(notebook)
            page = E.page()
            notebook.append(page)
            group = E.group()
            page.append(group)
            if self.model_id.is_mail_thread:
                chatter = E.div(klass="oe_chatter")
                chatter.append(
                    E.field(
                        name="message_follower_ids",
                        options="{'post_refresh':True}",
                        groups="base.group_user",
                    )
                )
                chatter.append(E.field(name="message_ids"))
                if self.model_id.is_mail_activity:
                    chatter.append(E.field(name="activity_ids"))
            if self.model_id.transient:
                footer = E.footer()
                arch.append(footer)
            arch = group

        for f in fs:
            f_dict = {"name": f.name}
            if f.type == "many2many" and view_mode in ["form", "tree"]:
                f_dict["widget"] = "many2many_tags"
            arch.append(E.field(**f_dict))

        return view
