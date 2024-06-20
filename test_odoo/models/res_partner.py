from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class Pouetpouet(models.Model):
    _inherit = "res.partner"

    my_moddy = fields.Many2one("moddy")
