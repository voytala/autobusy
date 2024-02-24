import json
import pandas as pd
from datetime import datetime
import numpy as np

def filter_data(json_file_path):
    # Wczytaj dane z pliku JSON do ramki danych
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Sprawdź, czy dane zawierają klucz "result"
    if 'result' in data:
        # Konwertuj listę wyników na ramkę danych
        df = pd.DataFrame(data['result'])
        
        # Sprawdź, czy kolumna "Time" istnieje w ramce danych
        df = df[df['Time'].str.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')]
        
        return df
    else:
        print("Brak klucza 'result' w pliku JSON.")
        return pd.DataFrame()  # Zwróć pustą ramkę danych w przypadku braku danych
    
def get_coords(df, zespol, slupek):
    # Wybierz wiersz spełniający warunki zespolu i slupka
    wiersz = df[(df['zespol'] == zespol) & (df['slupek'] == slupek)]
    # Sprawdź, czy znaleziono wiersz
    if not wiersz.empty:
        # Pobierz współrzędne
        szer_geo = wiersz['szer_geo'].iloc[0]  # Pierwszy element z kolumny szer_geo
        dlug_geo = wiersz['dlug_geo'].iloc[0]  # Pierwszy element z kolumny dlug_geo
        return szer_geo, dlug_geo
    else:
        # Jeśli nie znaleziono wiersza, zwróć None
        return None, None
def distance(lonA, latA, lonB, latB):
    R = 6371000  # Promień Ziemi w metrach
    lonA, latA, lonB, latB = map(np.radians, [lonA, latA, lonB, latB])
    dlon = lonB - lonA
    dlat = latB - latA
    a = np.sin(dlat/2.0)**2 + np.cos(latA) * np.cos(latB) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def speed(distAB, timeA, timeB):
    dtA = datetime.strptime(timeA, "%Y-%m-%d %H:%M:%S")
    dtB = datetime.strptime(timeB, "%Y-%m-%d %H:%M:%S")
    sec = abs((dtB - dtA).seconds)
    if sec > 0:
        return distAB / 1000 / sec * 3600
    else:
        return 0
