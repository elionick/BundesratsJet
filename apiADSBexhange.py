import requests
from env_vars import *
from datetime import datetime

def get_flight_data(icao):
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/hex/{icao}/"
    
    headers = {
        "X-RapidAPI-Key": apiADSB_key,
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:

        data = response.json()
        registration = data.get('r', None)
        flight = data.get('flight', None)
        type = data.get('t', None)
        latitude = data.get('lat', None)
        longitude = data.get('lon', None)
        altitude = data.get('alt_baro', 'ground')
        groundspeed = data.get('gs', 0)

        time = int(datetime.now().timestamp())

        #Testing only
        #print(icao, registration, type, time, latitude, longitude, altitude, groundspeed)

        return(icao, registration, type, flight, time, latitude, longitude, altitude, groundspeed)
    else:
        print(f'ADSB status: ' + str(response.status_code) + '. Response: ' + response.text)
        #return None