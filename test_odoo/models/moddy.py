from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class Moddy(models.Model):
    _name = "moddy"
    _description = "Soyez Moddy !"

    nom = fields.Char(string="Moddy Name", required=True)
    date = fields.Date()
    bool = fields.Boolean()
    lien_contact = fields.Many2one("res.partner")
    liste_pouets = fields.One2many("res.partner", "my_moddy")


# $    liste_produits = fields.pouet()
