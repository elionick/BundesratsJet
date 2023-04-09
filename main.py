from classAirplanes import Airplanes

#icao1 = "4b7f4c"
icao1 = "A87898"
#icao2 = "4b7fd4"
icao2 = "A27600"
db_path = "flights.db"

airplanes = Airplanes(icao1, icao2, db_path)

airplanes.check_flights()
