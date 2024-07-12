from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from ..fields import new_field
import logging
import string


class Partner(models.Model):
    _inherit = "res.partner"

    #    my_field = fields.Float(compute="compute_rate", inverse="inverse_rate")
    user_input = fields.Char(compute="compute_input", inverse="compute_rate")
    rate = fields.Float()

    def compute_rate(self):
        logging.info("COMPUTE RAAAAAAATE")
        bdd_value = 12.0
        for record in self:
            logging.info(record.user_input)
            if record.user_input != False:
                record.user_input = adapt_input(record.user_input)
                record.rate = float(record.user_input)
            else:
                record.rate = bdd_value

    def compute_input(self):
        logging.info("COMPUTE INPUUUUUUUUT")
        for record in self:
            logging.info(record.rate)
            record.user_input = str(record.rate)


def adapt_input(input_string):
    letters = string.ascii_letters
    for character in input_string:
        if character in letters:
            input_string = input_string.replace(character, "")
    return input_string
