import time
import sqlite3
from datetime import datetime, timezone
from apiADSBexhange import get_flight_data

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
                print(f'Attempting to get the data for {icao}')
                data = get_flight_data(icao)
                print(data)
                
                if data:
                    self.save_flight_data(data)
                    if self.check_flight_status(icao, data):
                        print(f"Flight {icao} took off at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(10)

    def save_flight_data(self, data):
        self.cursor.execute('INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    #Check if the airplane has taken off since last entry
    def check_flight_status(self, icao, data):
        last_data = self.get_last_flight_data(icao)
        if last_data:
            current_data = data
            if current_data[6] != "Ground" and last_data[6] == "Ground":
                return True
            return False

    def get_last_flight_data(self, icao):
        self.cursor.execute('SELECT * FROM flights WHERE icao=? ORDER BY time DESC LIMIT 1', (icao,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return None
        
    def close_connection(self):
        self.conn.close()