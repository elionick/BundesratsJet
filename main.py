from classAirplanes import Airplanes
from plotMap import plot_flight_plan
from apiTwitter import *

# Bundesratsjets:
# Dassault = "4b7f4c"
# Cessna = "4b7fd4"

airplanes = Airplanes(['4b7f4c', '4b7fd4'])

airplanes.check_flights()