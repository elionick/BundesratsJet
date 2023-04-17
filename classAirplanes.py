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
        self.create_flight_path_table()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS flights (icao TEXT, registration TEXT, type TEXT, time INTEGER, latitude REAL, longitude REAL, altitude TEXT, groundspeed REAL)')

    def create_flight_path_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS flight_path (flight_id INTEGER, icao TEXT, time INTEGER, latitude REAL, longitude REAL)')
    
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
                    #print(data)
                    #airport = get_airport_by_coordinates(data[4], data[5])
                    #airport_data = get_airport_data(airport[0])
                    #print(airport_data)
                    
                    print(status)
                    if status == 0: # Ground
                        print(f"Airplane {icao} is on the ground.")
                    elif status == 1: # Take-off
                        print(f"Airplane {icao} just took off")
                        self.start_flight_path(icao, data)
                        #update_Twitter_status(f"Airplane {icao} took off at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    elif status == 2: # In-Air
                        print(f"Airplane {icao} is at cruising altitude.")
                        self.save_flight_path(icao, data)
                    elif status == 3: # Landing
                        print(f"Airplane {icao} just landed")
                        self.save_flight_path(icao, data)
                        self.stop_flight_path(icao)
                    else:
                        None 

                
            time.sleep(300)

    #Section on tracking active flight path
    def start_flight_path(self, icao, data):
        index = self.get_last_flight_path_index(icao)
        if index is None:
            index = 1
        else:
            index += 1
        timestamp = data[3]
        latitude = data[4]
        longitude = data[5]
        self.cursor.execute('INSERT INTO flight_path VALUES (?, ?, ?, ?, ?)', (index, icao, timestamp, latitude, longitude))
        print(f'Started tracking flight path for {icao}')
        self.conn.commit()

    def save_flight_path(self, icao, data):
        index = self.get_last_flight_path_index(icao)
        timestamp = data[3]
        latitude = data[4]
        longitude = data[5]
        self.cursor.execute('INSERT INTO flight_path VALUES (?, ?, ?, ?, ?)', (index, icao, timestamp, latitude, longitude))
        self.conn.commit()
        
    def stop_flight_path(self, icao):
        print(f'Stopped tracking flight path for {icao}')


    def get_last_flight_path_index(self, icao):
        self.cursor.execute('SELECT MAX(flight_id) FROM flight_path WHERE icao=?', (icao,))
        index = self.cursor.fetchone()[0]
        if index:
            return index
        else:
            return None

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
        
    def save_flight_data(self, data):
        self.cursor.execute('INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    def get_last_flight_data(self, icao):
        self.cursor.execute('SELECT * FROM flights WHERE icao=? ORDER BY time DESC LIMIT 1 OFFSET 1', (icao,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return None
        
    def close_connection(self):
        self.conn.close()