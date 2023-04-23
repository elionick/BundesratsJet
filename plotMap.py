import sqlite3
import folium
from apiAirportData import *
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions


def plot_flight_plan(icao, flight_index):

    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()

    cursor.execute('SELECT latitude, longitude FROM flight_path WHERE flight_id=? AND icao=?', (flight_index, icao))

    coords = cursor.fetchall()
    conn.close()

    #Get start and landing coordinates
    departure_coords = coords[0]
    arrival_coords = coords[-1]

    #Get airports
    departure_airport = get_airport_by_coordinates(departure_coords[0], departure_coords[1])
    arrival_airport = get_airport_by_coordinates(arrival_coords[0], arrival_coords[1])

    # Calculate the middle coordinates
    middle_lat = sum(coord[0] for coord in coords) / len(coords)
    middle_lon = sum(coord[1] for coord in coords) / len(coords)

    # Set zoom_start based on number of coordinates
    if len(coords) <= 12:
        zoom_start = 6
    elif len(coords) <= 18:
        zoom_start = 5
    else:
        zoom_start = 4

    flight_map = folium.Map(location=[middle_lat, middle_lon], zoom_start=zoom_start)

    # Add a line between the markers to represent the flight path
    folium.PolyLine(coords, color='red').add_to(flight_map)

    # Add a marker for the airports

    folium.Marker(location=[departure_coords[0], departure_coords[1]],
                  popup=folium.Popup(f'<strong>Departure: </strong> {departure_airport[0]} - {departure_airport[1]}', show=True, max_width=500),
                  icon=folium.Icon(color='blue', icon='plane', prefix='fa')).add_to(flight_map)
    folium.Marker(location=[arrival_coords[0], arrival_coords[1]], 
                  popup=folium.Popup(f'<strong>Arrival: </strong>{arrival_airport[0]} - {arrival_airport[1]}', show=True, max_width=400),
                  icon=folium.Icon(color='green', icon='plane')).add_to(flight_map)
    
    # map_path = f"flight_{icao}-{flight_index}.png"

    # Outputting the file as PNG in media folder

    try:   

        # Outputting the Folium Map as HTML file
        print('Creating Map...')
        delay=1
        output= os.path.join(os.getcwd(), 'raw-map-data', f"flight_{icao}-{flight_index}.html")
        
        #tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=output)
        flight_map.save(output)

        # Saving HTML as PNG to upload to Twitter
        print('Saving Map as PNG...')

        tmpurl = 'file://' + os.path.join(os.getcwd(), 'raw-map-data', f'flight_{icao}-{flight_index}.html')

        opts = FirefoxOptions()
        opts.add_argument('--headless')
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=opts)

        browser.get(tmpurl)
        
        #Give the map tiles some time to load
        time.sleep(delay)
        screenshot_path = os.path.join(os.getcwd(), '/media', f'flight_{icao}-{flight_index}.png')
        browser.save_screenshot(screenshot_path)
        browser.quit()
        print('Map created successfully')

    except Exception as e:
        print(f'An error has occured while saving the image. . Error: {e}')

    return departure_airport, arrival_airport