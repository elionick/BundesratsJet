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

        #print(response.json())
        data = response.json()
        registration = data['r']
        flight = data['flight']
        type = data['t']
        latitude = data['lat']
        longitude = data['lon']
        altitude = data['alt_baro']
        groundspeed = data['gs']
        time = int(datetime.now().timestamp())

        #Testing only
        #print(icao, registration, type, time, latitude, longitude, altitude, groundspeed)

        return(icao, registration, type, flight, time, latitude, longitude, altitude, groundspeed)
    else:
        print(f'ADSB response: ' + response.status_code + response.text)
        #return None