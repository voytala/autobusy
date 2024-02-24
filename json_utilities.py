import json
import os
import requests

APIKEY = "c78d8fe3-ba29-41a3-8fb5-de78e48582b4"
URL_PRZYSTANKI = "https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3"
URL_PRZYSTANKI_BIEZ = "https://api.um.warszawa.pl/api/action/dbstore_get?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630"
URL_LINIE_PRZYSTANKU = "https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942"
URL_LINIE_ROZKLAD = "https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238"
URL_AUTOBUSY = "https://api.um.warszawa.pl/api/action/busestrams_get?resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59&type=1"
URL_SCHEDULES = "https://api.um.warszawa.pl/api/action/public_transport_routes/"

def get_json(url):
    try:
        response = requests.post(f"{url}&apikey={APIKEY}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error", err)
        raise SystemExit(err)

def save_json(json_response, fname):
    print(f"{fname} ", end="")
    fout = open(fname, 'wt')
    fout.write(json.dumps(json_response, indent=2))
    fout.close()
    fsize = os.path.getsize(fname)
    print(f"{fsize} OK")
    return fsize