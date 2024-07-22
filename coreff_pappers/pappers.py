import requests
import json
import base64


def clean_code(code):
    """Removes any non-numerical character and returns a string"""
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    cleaned_code = ""

    for character in code:
        if character in numbers:
            cleaned_code += character
    return cleaned_code


def search_report(api_token, company_code, code_type):
    lien = (
        "https://api.pappers.fr/v2/document/extrait_pappers?api_token="
        + api_token
        + "&"
        + code_type
        + "="
        + company_code
    )
    headers = {"Content": "application/json"}
    pdf = requests.get(lien, headers=headers)
    return base64.b64encode(pdf.content)


def search_directors(api_token, search_value):
    """Send a siret request and returns directors' infos as a list of dictionaries"""
    headers = {"Content": "application/json"}
    request = (
        "https://api.pappers.fr/v2/entreprise?api_token="
        + api_token
        + "&siret="
        + search_value
    )
    response = requests.get(request, headers=headers)
    directors = parse_search_directors(response)
    return directors


def search_name(api_token, search_value, head_office_only):
    """Send a name search request and returns companies' infos as a list of dictionaries"""
    headers = {"Content": "application/json"}
    request = (
        "https://api.pappers.fr/v2/recherche?api_token="
        + api_token
        + "&q="
        + search_value
        + "&siege="
        + str(
            head_office_only
        ).lower()  #! -> pas de différence sur l'api car renvoie uniquement des sièges quoi qu'il arrive
    )
    response = requests.get(request, headers=headers)
    suggestions = parse_search_name(response)
    return suggestions


def search_code(api_token, search_value, head_office_only):
    """Send a siret/siren search request and returns companies' infos as a list of dictionaries"""
    search_value = clean_code(search_value)
    headers = {"Content": "application/json"}
    suggestions = []
    if 9 <= len(search_value) < 14:
        request = (
            "https://api.pappers.fr/v2/entreprise?api_token="
            + api_token
            + "&siren="
            + search_value
        )
        response = requests.get(request, headers=headers)
        suggestions = parse_search_siren(response, head_office_only)
    elif len(search_value) == 14:
        request = (
            "https://api.pappers.fr/v2/entreprise?api_token="
            + api_token
            + "&siret="
            + search_value
        )
        response = requests.get(request, headers=headers)
        suggestions = parse_search_siret(response)
    return suggestions


def parse_search_directors(response):
    """Takes the response json and returns directors' infos as a list of dictionaries"""
    directors = []
    response = json.loads(response.text)
    for result in response["representants"]:
        director = {}
        director["name"] = result["nom_complet"]
        director["job"] = result["qualite"]
        director["street"] = result["adresse_ligne_1"]
        director["zip"] = result["code_postal"]
        director["city"] = result["ville"]
        directors.append(director)
    return directors


def parse_search_name(responseObject):
    """Takes the response json and returns companies' infos as a list of dictionaries"""
    suggestions = []
    response = json.loads(responseObject.text)
    for result in response["resultats"]:
        suggestion = {}
        suggestion["coreff_company_code"] = result["siren"]
        suggestion["name"] = result["nom_entreprise"]
        suggestion["street"] = result["siege"]["adresse_ligne_1"]
        suggestion["street2"] = result["siege"]["adresse_ligne_2"]
        suggestion["city"] = result["siege"]["ville"]
        suggestion["zip"] = result["siege"]["code_postal"]
        suggestion["pappers_json"] = responseObject.text
        suggestions.append(suggestion)
    return suggestions


def parse_search_siren(responseObject, head_office_only):
    """Takes the response json and returns companies' infos as a list of dictionaries"""
    suggestions = []
    response = json.loads(responseObject.text)
    for establishment in response["etablissements"]:
        suggestion = {}
        suggestion["coreff_company_code"] = establishment["siret"]
        suggestion["street"] = establishment["adresse_ligne_1"]
        suggestion["street2"] = establishment["adresse_ligne_2"]
        suggestion["city"] = establishment["ville"]
        suggestion["zip"] = establishment["code_postal"]
        suggestion["country_id"] = establishment["code_pays"]
        suggestion["name"] = response["nom_entreprise"]
        suggestion["vat"] = response["numero_tva_intracommunautaire"]
        suggestion["pappers_json"] = responseObject.text
        if (
            head_office_only == False or establishment["siege"] == True
        ) and establishment["etablissement_cesse"] == False:
            suggestions.append(suggestion)
    return suggestions


def parse_search_siret(responseObject):
    """Takes the response json and returns companies' infos as a list of dictionaries"""
    suggestions = []
    response = json.loads(responseObject.text)
    suggestion = {}
    suggestion["coreff_company_code"] = response["etablissement"]["siret"]
    suggestion["name"] = response["nom_entreprise"]
    suggestion["street"] = response["etablissement"]["adresse_ligne_1"]
    suggestion["street2"] = response["etablissement"]["adresse_ligne_2"]
    suggestion["city"] = response["etablissement"]["ville"]
    suggestion["zip"] = response["etablissement"]["code_postal"]
    suggestion["country_id"] = response["code_pays"]
    suggestion["vat"] = response["numero_tva_intracommunautaire"]
    suggestion["pappers_json"] = response.text
    suggestions.append(suggestion)
    return suggestions
