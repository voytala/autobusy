import time
from datetime import datetime
import requests
import json
import os
from json_utilities import APIKEY, get_json, save_json, URL_PRZYSTANKI, URL_PRZYSTANKI_BIEZ, URL_LINIE_ROZKLAD, URL_LINIE_PRZYSTANKU


SLEEP_TIME = 60
# EMPTY_RESULT = '{"result": "B\u0142\u0119dna metoda lub parametry wywo\u0142ania}'
    
#########################################################################################
# Przystanki

przystanki = get_json(URL_PRZYSTANKI)
save_json(przystanki, f"przystanki.json")
przystanki_biez = get_json(URL_PRZYSTANKI_BIEZ)
save_json(przystanki_biez, f"przystanki_biez.json")

#########################################################################################
# Rokłady linii na przystankach
#przystanki = json.loads('{"result": [{"values": [{"value": "1001", "key": "zespol"}, {"value": "01", "key": "slupek"}, {"value": "Kijowska", "key": "nazwa_zespolu"}, {"value": "2201", "key": "id_ulicy"}, {"value": "52.248455", "key": "szer_geo"}, {"value": "21.044827", "key": "dlug_geo"}, {"value": "al.Zieleniecka", "key": "kierunek"}, {"value": "2023-10-14 00:00:00.0", "key": "obowiazuje_od"}]}]}')

fout = open(f"przystanki_linie_rozklady.json", 'wt')
fout.write('{\n')
fout.write('  "result": [\n')
print("zespół słupek -> linia ...")
not_first_line = False
for p in przystanki['result']:    
    zespol = p["values"][0]["value"]
    slupek = p["values"][1]["value"]
    info = f"{zespol}   {slupek}     -> "
    print(f"{info}", end="")
    url = f"{URL_LINIE_PRZYSTANKU}&busstopId={zespol}&busstopNr={slupek}"
    linie_przystanku = get_json(url)
    for lp in linie_przystanku['result']:
        linia = lp["values"][0]["value"]
        info += linia + ' '
        print(f"\r{info}", end="")
        url = f"{URL_LINIE_ROZKLAD}&busstopId={zespol}&busstopNr={slupek}&line={linia}"
        rozklad_linii = get_json(url)
        json_rozklad_linii = ''
        for rl in rozklad_linii['result']:
            if not_first_line:
                json_rozklad_linii += ',\n'
            not_first_line = True
            json_rozklad_linii += '    {\n' + \
                                  '      "Zespol": "' + zespol + '",\n' + \
                                  '      "Slupek": "' + slupek + '",\n' + \
                                  '      "Linia": "' + linia + '",\n' + \
                                  '      "Brygada": "' + rl["values"][2]["value"] + '",\n' + \
                                  '      "Czas": "' + rl["values"][5]["value"] + '"\n' + \
                                  '    }'
        fout.write(json_rozklad_linii)
    print()
fout.write('\n  ]\n')
fout.write('}\n')
fout.close()