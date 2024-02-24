import os
import time
from json_utilities import save_json, get_json, URL_AUTOBUSY
from datetime import datetime

SLEEP_TIME = 60
BAD_REQUEST_COOLDOWN = 5
START_TIME = datetime.now()


def create_folder():
    # Utwórz folder na podstawie aktualnego czasu i daty
    folder_name = START_TIME.strftime("lokalizacja_%Y%m%d_%H%M%S")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def download_data(folder_name):
    for i in range(60):
        if i > 0:
            print(f"Sleeping {SLEEP_TIME} seconds ...")
            time.sleep(SLEEP_TIME)
        current_time = datetime.now()
        dt_string = current_time.strftime("%Y%m%d%H%M%S")
        fname = f"{folder_name}/autobusy_{dt_string}.json"
        print(f"{(i+1)} ", end="")
        locations = get_json(URL_AUTOBUSY)
        fsize = save_json(locations, fname)
        while fsize < 500:
            time.sleep(BAD_REQUEST_COOLDOWN)
            locations = get_json(URL_AUTOBUSY)
            fsize = save_json(locations, fname)


if __name__ == "__main__":
    folder_name = create_folder()
    download_data(folder_name)
