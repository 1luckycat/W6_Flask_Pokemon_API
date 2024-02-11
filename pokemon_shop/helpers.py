import requests
import requests_cache
import json
import os
import decimal

requests_cache.install_cache('pokemon_cache', backend='sqlite')

# Used google search api to get pokemon image
def get_image(search):
    url = "https://google-search72.p.rapidapi.com/imagesearch"

    querystring = {"q": search,"gl":"us","lr":"lang_en","num":"10","start":"0"}

    headers = {
	    "X-RapidAPI-Key": os.environ.get('api_key'),
	    "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    img_url = ""

    if 'items' in data.keys():
        img_url = data['items'][0]['originalImageUrl']
    return img_url



# Used rapidapi.com PokeAPI to get other Pokemon information
def get_ability(search):
    url = "https://pokemon-api3.p.rapidapi.com/pokemon"

    querystring = {"name": search.lower()}

    headers = {
        "X-RapidAPI-Key": os.environ.get('api_key'),
        "X-RapidAPI-Host": "pokemon-api3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    ability_url = ""

    if data:
        ability_url = [pokebility['ability']['name'] for pokebility in data['abilities']]
    return ability_url


def get_type(search):
    url = "https://pokemon-api3.p.rapidapi.com/pokemon"

    querystring = {"name": search.lower()}

    headers = {
        "X-RapidAPI-Key": os.environ.get('api_key'),
        "X-RapidAPI-Host": "pokemon-api3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    type_url = ""

    if data:
         type_url = [type_['type']['name'] for type_ in data['types']]
    return type_url


def get_height(search):
    url = "https://pokemon-api3.p.rapidapi.com/pokemon"

    querystring = {"name": search.lower()}

    headers = {
        "X-RapidAPI-Key": os.environ.get('api_key'),
        "X-RapidAPI-Host": "pokemon-api3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    height_url = ""

    if data:
        height_url = data['height']
    return height_url


def get_weight(search):
    url = "https://pokemon-api3.p.rapidapi.com/pokemon"

    querystring = {"name": search.lower()}

    headers = {
        "X-RapidAPI-Key": os.environ.get('api_key'),
        "X-RapidAPI-Host": "pokemon-api3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    weight_url = ""

    if data:
        weight_url = data['weight']
    return weight_url



class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)





