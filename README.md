
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/lambdao-dev/odoo-dev-tools/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/lambdao-dev/odoo-dev-tools/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/lambdao-dev/odoo-dev-tools/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/lambdao-dev/odoo-dev-tools/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/lambdao-dev/odoo-dev-tools/branch/16.0/graph/badge.svg)](https://codecov.io/gh/lambdao-dev/odoo-dev-tools)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Odoo Development Tools

Odoo addons to ease the development experience

## Installation

You can simply install these modules like every other Odoo module; either manually or through the pip tools.

## Usage

The modules in this repository are meant to be used by developers, and are not meant to be used by end users.
Some, like `base_pretty_print`, only offer functions to be used in shell mode.
Others include a wizard that can be used via the GUI.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_ir_export](base_ir_export/) | 16.0.1.0.0 |  | Module providing a wizard to create exports and views on ir.exports
[base_pretty_print](base_pretty_print/) | 16.0.1.0.0 |  | Base module that provide display functions on the base model
[base_viewify](base_viewify/) | 16.0.1.0.0 |  | Base module to generate Odoo views
[base_xmlify](base_xmlify/) | 16.0.1.0.0 |  | Base module that provide an xmlify method on all models

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to len-foss
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->
