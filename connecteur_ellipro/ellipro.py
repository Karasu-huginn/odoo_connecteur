import requests
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum


class IdType(Enum):
    REGISTER = "register"
    SRC = "src"
    ESTB = "register-estb"
    VAT = "vat"


class SearchType(Enum):
    ID = 0
    NAME = 1


class RequestType(Enum):
    SEARCH = "svcSearch"
    ONLINEORDER = "svcOnlineOrder"
    CATALOGUE = "svcCatalogue"


@dataclass
class Admin:
    contract_id: str
    user_id: str
    password: str

    def set_element(self, root):
        admin = ET.SubElement(root, "admin")
        client = ET.SubElement(admin, "client")
        context = ET.SubElement(admin, "context")
        ET.SubElement(client, "contractId").text = self.contract_id
        ET.SubElement(client, "userId").text = self.user_id
        ET.SubElement(client, "password").text = self.password
        ET.SubElement(context, "appId", attrib={"version": "1"}).text = "WSRISK"
        ET.SubElement(context, "date").text = "2013-11-05T17:38:15+01:00"


@dataclass
class Search:
    search_type: SearchType
    search_text: str
    max_hits: str
    type_attribute: IdType
    main_only = "true"
    custom_content = "false"
    company_status = "active"
    establishment_status = "active"
    phonetic_search = "false"

    def set_element(self, root):
        request = ET.SubElement(root, "request")

        search_criteria = ET.SubElement(request, "searchCriteria")
        if self.search_type == SearchType.ID:
            ET.SubElement(
                search_criteria, "id", attrib={"type": self.type_attribute.value}
            ).text = self.search_text
        elif self.search_type == SearchType.NAME:
            ET.SubElement(search_criteria, "name").text = self.search_text
        address = ET.SubElement(search_criteria, "address")
        ET.SubElement(address, "country", attrib={"code": "FRA"})

        search_options = ET.SubElement(request, "searchOptions")
        ET.SubElement(search_options, "phoneticSearch").text = self.phonetic_search
        ET.SubElement(search_options, "maxHits").text = self.max_hits
        ET.SubElement(search_options, "mainOnly").text = self.main_only
        ET.SubElement(search_options, "customContent").text = self.custom_content
        ET.SubElement(search_options, "companyStatus").text = self.company_status
        ET.SubElement(search_options, "establishmentStatus").text = (
            self.establishment_status
        )


@dataclass
class Order:
    company_id: str
    product_id: str
    product_version = "1"
    currency = "EUR"
    monitoring_requested = "false"
    output_method = "raw"
    format = "XML"

    def set_element(self, root):
        request = ET.SubElement(root, "request")
        ET.SubElement(request, "country", attrib={"code": "FRA"})
        ET.SubElement(request, "id", attrib={"type": "src"}).text = self.company_id
        ET.SubElement(
            request,
            "product",
            attrib={"range": self.product_id, "version": self.product_version},
        )
        #!order_options = ET.SubElement(request, "orderOptions")
        #!ET.SubElement(order_options, "currency").text = self.currency
        #!ET.SubElement(order_options, "monitoringRequested").text = (
        #!    self.monitoring_requested
        #!)
        # $ financials = ET.SubElement(order_options, "financials")
        # $ ET.SubElement(financials, "year")
        # $ ET.SubElement(financials, "date")
        # $ ET.SubElement(financials, "option").text = "LAST"  #! var
        # $ ET.SubElement(financials, "numberOfYears")
        # $ ET.SubElement(financials, "numberOfAccounts")
        delivery_options = ET.SubElement(request, "deliveryOptions")
        ET.SubElement(delivery_options, "outputMethod").text = self.output_method
        ET.SubElement(delivery_options, "format").text = self.format


@dataclass
class Catalogue:
    company_id: str
    country_code = "FRA"

    def set_element(self, root):
        request = ET.SubElement(root, "request")
        ET.SubElement(request, "country", attrib={"code": self.country_code})
        ET.SubElement(request, "id", attrib={"type": "src"}).text = self.company_id


def get_company(admin, lang):
    root = ET.Element("", attrib={"lang": lang})
    admin.set_element(root)


def search(admin, search, lang="FR"):
    request_type = RequestType.SEARCH.value

    headers = {"Content-Type": "application/xml"}
    root = ET.Element(
        f"{request_type}Request", attrib={"lang": lang, "version": "2.2"}
    )  #! missing version
    admin.set_element(root)
    search.set_element(root)
    body = ET.tostring(root)

    request = requests.post(
        f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
        data=body,
        headers=headers,
    )
    return ET.fromstring(request.text)


def catalogue(admin, catalogue, request_type, lang="FR"):
    headers = {"Content-Type": "application/xml"}

    root = ET.Element(
        f"{request_type}Request", attrib={"lang": lang, "version": "2.2"}
    )  #! missing version
    admin.set_element(root)
    catalogue.set_element(root)
    body = ET.tostring(root)

    request = requests.post(
        f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
        data=body,
        headers=headers,
    )
    return ET.fromstring(request.text)


def order(admin, order, request_type, lang="FR"):
    headers = {"Content-Type": "application/xml"}

    root = ET.Element(
        f"{request_type}Request", attrib={"lang": lang, "version": "2.2"}
    )  #! missing version
    admin.set_element(root)
    order.set_element(root)
    body = ET.tostring(root)

    request = requests.post(
        f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
        data=body,
        headers=headers,
    )
    return ET.fromstring(request.text)


if __name__ == "__main__":

    request_type = RequestType.SEARCH

    admin = Admin("53560", "NN448142", "#Pa55word")

    if request_type == RequestType.SEARCH:
        search_text = input("Nom : ")
        search_request = Search(
            SearchType.NAME,
            search_text,
            "20",
            IdType.ESTB,
        )
        response = search(admin, search_request)
        # * print search
        businessName = ""
        tradeName = ""
        siren = ""
        siret = ""
        phoneNumber = ""
        suggestions = []
        ET.dump(response)
        for establishment in response.iter("establishment"):
            suggestion = {}
            suggestion["name"] = establishment.findall("name")[0].text
            suggestion["coreff_company_code"] = establishment.findall(
                "id[@idName='SIREN']"
            )[0].text
            suggestion["ellipro_siret"] = establishment.findall("id[@idName='SIRET']")[
                0
            ].text
            suggestion["ellipro_identifiant_interne"] = establishment.findall(
                "id[@idName='Identifiant interne']"
            )[0].text
            if establishment.findall("communication[@type='phone']") != []:
                suggestion["phone"] = establishment.findall(
                    "communication[@type='phone']"
                )[0].text
            suggestion["city"] = establishment.findall("address/cityName")[0].text
            suggestion["zip"] = establishment.findall("address/cityCode")[0].text
            suggestion["street"] = establishment.findall("address/addressLine")[0].text
            suggestion["ellipro_siren"] = establishment.findall("id[@idName='SIREN']")[
                0
            ].text
            if establishment.findall("name[@type='businessname']") != []:
                suggestion["ellipro_business_name"] = establishment.findall(
                    "name[@type='businessname']"
                )[0].text
            if establishment.findall("name[@type='tradename']") != []:
                suggestion["ellipro_trade_name"] = establishment.findall(
                    "name[@type='tradename']"
                )[0].text
            suggestion["ellipro_city"] = establishment.findall("address/cityName")[
                0
            ].text
            suggestion["ellipro_zipcode"] = establishment.findall("address/cityCode")[
                0
            ].text
            suggestion["ellipro_street_address"] = establishment.findall(
                "address/addressLine"
            )[0].text
            if establishment.findall("communication[@type='phone']") != []:
                suggestion["ellipro_phone_number"] = establishment.findall(
                    "communication[@type='phone']"
                )[0].text
            suggestions.append(suggestion)
            print(suggestion)
    elif request_type == RequestType.ONLINEORDER:
        company_id = input("Id interne : ")
        product_id = input("Id produit : ")
        order_request = Order(company_id, product_id)
        response = order(admin, order_request, request_type.value)
        # print(response.find("description").text)
    elif request_type == RequestType.CATALOGUE:
        company_id = input("Id interne : ")
        catalogue_request = Catalogue(company_id)
        response = catalogue(admin, catalogue_request, request_type.value)
        for element in response.iter("catalogueEntry"):
            print(
                element.findall("product")[0].text,
                element.findall("product")[0].attrib["range"],
            )


"""

































def xmlCreatorSearch(
    search_type,
    search_text,
    contract_id,
    user_id,
    password,
    lang,
    max_hits,
    type_attribute,
    main_only,
    custom_content,
    company_status,
    establishment_status,
    phonetic_search,
):
    search = ET.Element("svcSearchRequest", attrib={"lang": lang})
    admin = ET.SubElement(search, "admin")
    request = ET.SubElement(search, "request")
    client = ET.SubElement(admin, "client")
    context = ET.SubElement(admin, "context")
    ET.SubElement(client, "contractId").text = contract_id
    ET.SubElement(client, "userId").text = user_id
    ET.SubElement(client, "password").text = password
    ET.SubElement(context, "appId", attrib={"version": "1"}).text = "WSOM"
    ET.SubElement(context, "date").text = "2013-11-05T17:38:15+01:00"
    search_criteria = ET.SubElement(request, "searchCriteria")
    if type_attribute != None:
        ET.SubElement(
            search_criteria, search_type, attrib={"type": type_attribute}
        ).text = search_text
    else:
        ET.SubElement(search_criteria, search_type).text = search_text
    search_options = ET.SubElement(request, "searchOptions")
    ET.SubElement(search_options, "phoneticSearch").text = phonetic_search
    ET.SubElement(search_options, "maxHits").text = max_hits
    ET.SubElement(search_options, "mainOnly").text = main_only
    ET.SubElement(search_options, "customContent").text = custom_content
    ET.SubElement(search_options, "companyStatus").text = company_status
    ET.SubElement(search_options, "establishmentStatus").text = establishment_status
    search = ET.tostring(search)
    return search


def request_search(
    request_type,
    search_type,
    search_text,
    contract_id,
    user_id,
    password,
    lang,
    max_hits,
    type_attribute=None,
    main_only="true",
    custom_content="false",
    company_status="active",
    establishment_status="active",
    phonetic_search="false",
):
    body = xmlCreatorSearch(
        search_type,
        search_text,
        contract_id,
        user_id,
        password,
        lang,
        max_hits,
        type_attribute,
        main_only,
        custom_content,
        company_status,
        establishment_status,
        phonetic_search,
    )
    headers = {"Content-Type": "application/xml"}
    request = requests.post(
        f"https://services-test.data-access-gateway.com/1/rest/{request_type}",
        data=body,
        headers=headers,
    )
    root = ET.fromstring(request.text)
    return root"""
