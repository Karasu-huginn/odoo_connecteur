from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from ..ellipro import Admin, Search, Order, Catalogue, SearchType, IdType, RequestType
import xml.etree.ElementTree as ET
import requests


class ResPartner(models.Model):
    _inherit = "res.partner"

    ellipro_search_type = fields.Selection([("0", "ID"), ("1", "Name")], required=True)
    ellipro_search_text = fields.Char()
    ellipro_max_hits = fields.Char()
    ellipro_type_attribute = fields.Char()

    ellipro_order_company = fields.Char()
    ellipro_order_product = fields.Char()

    ellipro_search_result_siret = fields.Char()
    ellipro_search_result_name = fields.Char()

    ellipro_order_result = fields.Char()

    def search_button(self):
        request_type = RequestType.SEARCH.value
        search_type = SearchType(int(self.ellipro_search_type))

        admin = Admin("53560", "NN448142", "#Pa55word")

        search_request = Search(
            SearchType.NAME,
            self.ellipro_search_text,
            "1",
            IdType(self.ellipro_type_attribute),
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
        #        debug_text = request.text
        #        self.ellipro_search_result = debug_text

        response = ET.fromstring(request.text)

        for element in response.iter("establishment"):
            self.ellipro_search_result_name = element.findall("name")[0].text
            self.ellipro_search_result_siret = element.findall("id")[2].text

    def order_button(self):
        request_type = RequestType.ONLINEORDER.value
        order_request = Order(self.ellipro_order_company, self.ellipro_order_product)

        admin = Admin("53560", "NN448142", "#Pa55word")

        headers = {"Content-Type": "application/xml"}

        root = ET.Element(
            f"{request_type}Request", attrib={"lang": "FR", "version": "2.2"}
        )
        admin.set_element(root)
        order_request.set_element(root)
        body = ET.tostring(root)

        request = requests.post(
            f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
            data=body,
            headers=headers,
        )
        self.ellipro_order_result = request.text
