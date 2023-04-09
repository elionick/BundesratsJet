from env_vars import *
import time
from datetime import datetime, timezone, timedelta
from opensky_api import OpenSkyApi

# Set the airport code and time range for departures
airport_code = "LSZH" # Zurich Airport
begin_time = int((datetime.now() - timedelta(hours=10)).timestamp())
end_time = int((datetime.now() - timedelta(hours=8)).timestamp())

# Connect to the OpenSky Network API
api = OpenSkyApi()

departures = api.get_departures_by_airport(airport_code, begin_time, end_time)

print(departures)