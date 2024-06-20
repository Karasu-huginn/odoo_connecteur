from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ResCompany(models.TransientModel):
    _name = "ellipro.res.partner.create"

    ellipro_contract = fields.Char()
    ellipro_user = fields.Char()
    ellipro_password = fields.Char()
