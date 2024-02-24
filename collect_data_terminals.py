from json_utilities import get_json, save_json, URL_SCHEDULES

fname = f"schedules.json"
schedules = get_json(URL_SCHEDULES)
save_json(schedules, fname)