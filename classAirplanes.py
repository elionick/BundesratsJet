import time
import sqlite3
from datetime import datetime, timezone
from apiADSBexhange import get_flight_data
from apiTwitter import update_Twitter_status
from apiAirportData import *

class Airplanes:
    
    def __init__(self, icao_list):
        self.icao_list = icao_list
        self.db_path = "flights.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS flights (icao TEXT, registration TEXT, type TEXT, time INTEGER, latitude REAL, longitude REAL, altitude TEXT, groundspeed REAL)')

    def check_flights(self):
        while True:
            for icao in self.icao_list:
                print(f'Getting the data for {icao}')
                data = get_flight_data(icao)
                #Print data to inspect
                #print(data)

                if data:
                    self.save_flight_data(data)
                    status = self.check_flight_status(icao, data)
                    print(data)
                    airport = get_airport_by_coordinates(data[4], data[5])
                    airport_data = get_airport_data(airport[0])
                    print(airport_data)
                    
                    print(status)
                    if status == 0: # Ground
                        print(f"Airplane {icao} is on the ground.")
                    elif status == 1: # Take-off
                        print(f"Airplane {icao} just took off")
                        #update_Twitter_status(f"Airplane {icao} took off at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    elif status == 2: # In-Air
                        print(f"Airplane {icao} is at cruising altitude.")
                    elif status == 3: # Landing
                        print(f"Airplane {icao} just landed")
                    else:
                        None 

            time.sleep(60)

    def save_flight_data(self, data):
        self.cursor.execute('INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    #Check the latest status of the airplane in comparison to the previous database entry to determine it's flight phase
    def check_flight_status(self, icao, data):
        current_data = data
        last_data = self.get_last_flight_data(icao)
        if last_data:
            print(f"Last altitude: {last_data[6]}, Current altitude: {current_data[6]}")
            if last_data[6] == "ground" and current_data[6] == "ground":
                return 0 # Ground
            elif last_data[6] == "ground" and current_data[6] != "ground":
                return 1 # Take-off
            elif last_data[6] != "ground" and current_data[6] != "ground":
                return 2 # In-air
            elif last_data[6] != "ground" and current_data[6] == "ground":
                return 3 # Landing
        else:
            print('First time tracking this airplane')
            return None

    def get_last_flight_data(self, icao):
        self.cursor.execute('SELECT * FROM flights WHERE icao=? ORDER BY time DESC LIMIT 1 OFFSET 1', (icao,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return None
        
    def close_connection(self):
        self.conn.close()