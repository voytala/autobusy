from json_utilities import get_json, save_json
from json_utilities import URL_LINIE_ROZKLAD, URL_LINIE_PRZYSTANKU
from json_utilities import URL_PRZYSTANKI, URL_PRZYSTANKI_BIEZ

SLEEP_TIME = 60
#########################################################################################
# Przystanki

przystanki = get_json(URL_PRZYSTANKI)
save_json(przystanki, f"przystanki.json")
przystanki_biez = get_json(URL_PRZYSTANKI_BIEZ)
save_json(przystanki_biez, f"przystanki_biez.json")

#########################################################################################
# Rokłady linii na przystankach
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
