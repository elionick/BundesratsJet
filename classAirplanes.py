import time
import sqlite3
from datetime import datetime, timezone
from apiADSBexhange import get_flight_data
from apiTwitter import update_Twitter_status

class Airplanes:
    
    def __init__(self, icao1, icao2, db_path):
        self.icao1 = icao1
        self.icao2 = icao2
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS flights (icao TEXT, registration TEXT, type TEXT, time INTEGER, latitude REAL, longitude REAL, altitude BLOB, groundspeed REAL)')

    def check_flights(self):
        while True:
            for icao in [self.icao1, self.icao2]:
                print(f'Getting the data for {icao}')
                data = get_flight_data(icao)
                print(data)
                
                if data:
                    self.save_flight_data(data)
                    if self.check_flight_status(icao, data) == 0: # Ground
                        print(f"As of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, airplane {icao} is on the ground.")
                        #update_Twitter_status(f"As of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, airplane {icao} is on the ground.")
                    if self.check_flight_status(icao, data) == 1: # Take-off
                        print(f"Airplane {icao} took off at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        #update_Twitter_status(f"Airplane {icao} took off at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    if self.check_flight_status(icao, data) == 2: # In-Air
                        print(f"Airplane {icao} is at cruising altitude.")
                        #update_Twitter_status(f"Airplane {icao} is at cruising altitude.")
                    if self.check_flight_status(icao, data) == 3: # Landing
                        print(f"Airplane {icao} landed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        #update_Twitter_status(f"Airplane {icao} landed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            time.sleep(60)

    def save_flight_data(self, data):
        self.cursor.execute('INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    #Check the latest status of the airplane in comparison to the previous database entry to determine it's flight phase
    def check_flight_status(self, icao, data):
        last_data = self.get_last_flight_data(icao)
        if last_data:
            current_data = data
            if last_data[6] == "ground" and current_data[6] == "ground":
                return 0 # Ground
            if last_data[6] == "ground" and current_data[6] != "ground":
                return 1 # Take-off
            if last_data[6] != "ground" and current_data[6] != "ground":
                return 2 # In-air
            if last_data[6] != "ground" and current_data[6] == "ground":
                return 3 # Landing

    def get_last_flight_data(self, icao):
        self.cursor.execute('SELECT * FROM flights WHERE icao=? ORDER BY time DESC LIMIT 1', (icao,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return None
        
    def close_connection(self):
        self.conn.close()