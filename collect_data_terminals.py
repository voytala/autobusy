import time
import requests
from json_utilities import get_json, save_json, APIKEY, URL_SCHEDULES
from datetime import datetime
    
fname = f"schedules.json"
schedules = get_json(URL_SCHEDULES)
save_json(schedules, fname)