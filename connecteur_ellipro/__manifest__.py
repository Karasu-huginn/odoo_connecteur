# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "connecteur_ellipro",
    "version": "14.0.1.0.0",
    "summary": "",
    "description": "",
    "depends": ["base", "multi_step_wizard"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
        "views/ellipro_res_partner_create.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
