from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class PartnerResult(models.TransientModel):
    _name = "ellipro.partners.results"

    ellipro_search = fields.One2many(
        "ellipro.res.partner.create", "ellipro_results_list"
    )

    name = fields.Char()
    company_name = fields.Char()
    commercial_company_name = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    street = fields.Char()
    phone = fields.Char()
    ellipro_search_result_siren = fields.Char()
    ellipro_search_result_siret = fields.Char()


#    ellipro_search = fields.Many2one("ellipro.res.partner.create")
