from env_vars import *
import time
from datetime import datetime, timezone, timedelta
from opensky_api import OpenSkyApi
from pprint import pprint

# Set the airport code and time range for departures
airport_code = "LSZH" # Zurich Airport
begin_time = int((datetime.now() - timedelta(hours=1)).timestamp())
end_time = int(datetime.now().timestamp())

# Connect to the OpenSky Network API
api = OpenSkyApi(api_user,api_password)

departures = api.get_departures_by_airport(airport_code, begin_time, end_time)

pprint(departures)
