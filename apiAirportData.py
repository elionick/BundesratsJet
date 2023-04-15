import requests
from bs4 import BeautifulSoup
from env_vars import *

def get_airport_by_coordinates(lat, lon):

    # Make the GET request and parse the response with BeautifulSoup
    url = f'https://ourairports.com/search?q={lat}+{lon}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find("section", class_='airport listing row')

    # Extract the airport code and name
    airport_icao = results.find('a').get('href').split('/')[-2].upper()
    airport_name = results.find('h3').text.strip()
    
    print(f"Airport code: {airport_icao}")
    print(f"Airport name: {airport_name}")

    return airport_icao, airport_name

def get_airport_data(airport_icao):

    #Use the Airport-Info API to get further inforamtion on an airport using ICAO code
    url = "https://airport-info.p.rapidapi.com/airport"

    querystring = {'icao':{airport_icao}}

    headers = {
        "X-RapidAPI-Key": apiADSB_key,
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #Save and return interesting data
    data = response.json()
    name = data['name']
    location = data['location']
    country_iso = data['country_iso']
    country = data['country']

    return name, location, country_iso, country
