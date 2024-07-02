from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    ellipro_contract = fields.Char()
    ellipro_user = fields.Char()
    ellipro_password = fields.Char()
    ellipro_max_hits = fields.Char()
