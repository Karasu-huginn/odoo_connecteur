from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import logging
from .. import ellipro as EP
import xml.etree.ElementTree as ET
import requests

logger = logging.getLogger()


class ResPartner(models.TransientModel):
    _name = "ellipro.res.partner.create"
    _inherit = ["multi.step.wizard.mixin"]

    ellipro_search_type = fields.Selection(
        [("0", "ID"), ("1", "Name")], required=True, default="1"
    )
    ellipro_search_text = fields.Char()
    ellipro_type_attribute = fields.Selection(
        [
            ("register", "SIREN"),
            ("register-estb", "SIRET"),
            ("vat", "Numéro TVA"),
        ],
        required=True,
        default="register",
    )

    ellipro_results_list = fields.Many2one("ellipro.partners.results")

    ellipro_predict = fields.Char()

    ellipro_search_result_siret = fields.Char()
    ellipro_search_result_siren = fields.Char()
    ellipro_name = fields.Char()
    ellipro_business_name = fields.Char()
    ellipro_trade_name = fields.Char()
    ellipro_city = fields.Char()
    ellipro_zipcode = fields.Char()
    ellipro_street_address = fields.Char()
    ellipro_phone_number = fields.Char()

    @api.model
    def _selection_state(self):
        return [
            ("start", "Start"),
            ("configure", "Configure"),
            ("final", "Final"),
        ]

    @api.model
    def _default_project_id(self):
        logger.info(self.env.context.get("active_id"))
        return self.env.context.get("active_id")

    def state_exit_start(self):
        self.create_partner_action()
        self.state = "configure"

    def state_exit_configure(self):
        result_id = self.ellipro_results_list["id"]
        logger.info(self.ellipro_results_list.name)
        create_values = {
            "name": self.ellipro_results_list.name,
            "company_name": self.ellipro_results_list.company_name,
            "commercial_company_name": self.ellipro_results_list.commercial_company_name,
            "city": self.ellipro_results_list.city,
            "zip": self.ellipro_results_list.zip,
            "street": self.ellipro_results_list.street,
            "phone": self.ellipro_results_list.phone,
            "ellipro_search_result_siret": self.ellipro_results_list.ellipro_search_result_siret,
            "ellipro_search_result_siren": self.ellipro_results_list.ellipro_search_result_siren,
        }
        record_id = self.env["res.partner"].create(create_values)
        self.state = "final"
        # ? return {
        # ?     "name": _("Partner"),
        # ?     "view_type": "form",
        # ?     "view_mode": "form",
        # ?     "view_id": False,
        # ?     "res_model": "res.partner",
        # ?     "res_id": record_id.id,
        # ?     "context": self.env.context,
        # ?     "type": "ir.actions.act_window",
        # ?     "target": "current",
        # ? }

    def create_partner_action(self):
        self.env["ellipro.partners.results"].sudo().with_context(
            active_test=False
        ).search([]).unlink()
        request_type = EP.RequestType.SEARCH.value
        search_type = EP.SearchType(int(self.ellipro_search_type))
        type_attribute = EP.IdType(self.ellipro_type_attribute)

        admin = EP.Admin(
            self.env.user.company_id.ellipro_contract,
            self.env.user.company_id.ellipro_user,
            self.env.user.company_id.ellipro_password,
        )

        search_request = EP.Search(
            search_type,
            self.ellipro_search_text,
            self.env.user.company_id.ellipro_max_hits,
            type_attribute,  # todo
        )

        headers = {"Content-Type": "application/xml"}

        root = ET.Element(
            f"{request_type}Request", attrib={"lang": "FR", "version": "2.2"}
        )
        admin.set_element(root)
        search_request.set_element(root)
        body = ET.tostring(root)

        request = requests.post(
            f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
            data=body,
            headers=headers,
        )

        response = ET.fromstring(request.text)
        logger.info(request.text)

        for establishment in response.iter("establishment"):
            names = establishment.findall("name")
            self.ellipro_name = names[0].text
            self.write({"ellipro_predict": names[0].text})
            for name in names:
                if name.attrib["type"] == "businessname":
                    self.ellipro_business_name = name.text
                elif name.attrib["type"] == "tradename":
                    self.ellipro_trade_name = name.text
            ids = establishment.findall("id")
            for id in ids:
                if id.attrib["idName"] == "SIREN":
                    self.ellipro_search_result_siren = id.text
                elif id.attrib["idName"] == "SIRET":
                    self.ellipro_search_result_siret = id.text
            communications = establishment.findall("communication")
            for number in communications:
                if number.attrib["type"] == "phone":
                    self.ellipro_phone_number = number.text
            for address in response.iter("address"):
                self.ellipro_city = address.findall("cityName")[0].text
                self.ellipro_zipcode = address.findall("cityCode")[0].text
                self.ellipro_street_address = address.findall("addressLine")[0].text

            create_values = {
                "name": self.ellipro_name,
                "company_name": self.ellipro_business_name,
                "commercial_company_name": self.ellipro_trade_name,
                "city": self.ellipro_city,
                "zip": self.ellipro_zipcode,
                "street": self.ellipro_street_address,
                "phone": self.ellipro_phone_number,
                "ellipro_search_result_siret": self.ellipro_search_result_siret,
                "ellipro_search_result_siren": self.ellipro_search_result_siren,
            }
            record_id = self.env["ellipro.partners.results"].create(create_values)

    def cancel_partner_action(self):
        pass


# //        logger.info(
# //            "\n-------------------------------\nstate_exit_configure\n-------------------------------"
# //        )
