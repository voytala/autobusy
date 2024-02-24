from speed import distance
import pandas as pd
import ijson
import json
from datetime import datetime, timedelta
from math import ceil
import os
import sys
from speed_common import filter_data, get_coords

if len(sys.argv) != 2:
    print("Podaj nazwę katalogu zawierającego pliki JSON.")
    sys.exit(1)

# Odczytaj nazwę katalogu z argumentu linii poleceń
folder_name = sys.argv[1]


# Funkcja do przekształcenia daty z nazwy folderu
def transform_folder_date(folder_name):
    try:
        time_obj = datetime.strptime(folder_name.split('_')[2], "%H%M%S")
        return time_obj.strftime("%H:%M:%S")
    except Exception as e:
        print("Nieprawidłowa nazwa folderu. Oczekiwany format: lokalizacja_YYYYMMDD_HHMMSS")
        raise e


BEGIN_DATE_STRING = transform_folder_date(folder_name)

# Podział stringa na godzinę, minutę i sekundę
hour, minute, second = map(int, BEGIN_DATE_STRING.split(':'))

# Dodanie 2 do godziny
hour += 2

# Nowy string godziny
END_DATE_STRING = f'{hour:02d}:{minute:02d}:{second:02d}'

json_file_path = "przystanki_linie_rozklady.json"

# Wczytaj i przefiltruj dane z dużego pliku JSON przy użyciu ijson
filtered_data = []
with open(json_file_path, 'r') as file:
    for item in ijson.items(file, 'result.item'):
        if all(key in item for key in ('Linia', 'Brygada', 'Czas')):
            if 'Czas' in item and item['Czas'] > BEGIN_DATE_STRING and item['Czas'] < END_DATE_STRING:
                filtered_data.append({
                    'Linia': item['Linia'],
                    'Brygada': item['Brygada'],
                    'Zespol': item.get('Zespol', None),
                    'Slupek': str(item.get('Slupek', None)),  # Konwersja na string
                    'Czas': item['Czas']
                })

df_rozklady = pd.DataFrame(filtered_data)
df_rozklady.drop_duplicates(inplace=True)
df_rozklady.sort_values(by=['Linia', 'Brygada', 'Czas'], inplace=True)


def find_next_stop(df, linia, brygada, czas):
    subset = df[(df['Linia'] == linia) & (df['Brygada'] == brygada) & (df['Czas'] > czas)]
    if subset.empty:
        return None, None, None
    next_time_row = subset.iloc[0]
    return next_time_row['Czas'], next_time_row['Slupek'], next_time_row['Zespol']


with open('przystanki.json', 'r') as f:
    data = json.load(f)

rows = []

for result in data['result']:
    values_dict = {}
    for value in result['values']:
        values_dict[value['key']] = value['value']
    rows.append(values_dict)

df_przystanki = pd.DataFrame(rows)


def transform_date_format(date_str):
    date_time_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    time_str = date_time_obj.strftime("%H:%M:%S")
    return time_str

# Wczytaj dane z plików JSON w podanym katalogu
files = os.listdir(folder_name)
files.sort()

# Słownik przechowujący informacje o opóźnieniach autobusów
opoznienia = {}

# Słownik przechowujący informacje o opóźnieniach autobusów
wyniki_analizy = []

for i in range(len(files) - 1):
    print(f"Migawka {i}")
    file_path_1 = os.path.join(folder_name, files[i])
    file_path_2 = os.path.join(folder_name, files[i+1])

    df_1 = filter_data(file_path_1)
    df_2 = filter_data(file_path_2)

    df_1['Time'] = df_1['Time'].apply(transform_date_format)
    df_2['Time'] = df_2['Time'].apply(transform_date_format)

    df_filtered_1 = df_1[(df_1['Time'] >= BEGIN_DATE_STRING)]
    df_filtered_2 = df_2[(df_2['Time'] >= BEGIN_DATE_STRING)]

    for _, row in df_filtered_2.iterrows():
        linia = row['Lines']
        brygada = row['Brigade']
        czas_str = row['Time']
        # Sprawdź, czy istnieje wiersz dla danego autobusu w poprzedniej migawce
        autobus_i_wiersz = df_1[(df_1['Lines'] == linia) & (df_1['Brigade'] == brygada)]
        if autobus_i_wiersz.empty:
            print(f"Brak danych dla autobusu o linii {linia} i brygadzie {brygada} w poprzedniej migawce. Pomijam analizę tego autobusu.")
            continue

        if (linia, brygada) in opoznienia:
            next_time_str = opoznienia[(linia, brygada)]['next_time_str']
            slupek = opoznienia[(linia, brygada)]['slupek']
            zespol = opoznienia[(linia, brygada)]['zespol']
        else:
            next_time_str, slupek, zespol = find_next_stop(df_rozklady, linia, brygada, czas_str)

        if next_time_str is not None:
            #next_time = datetime.strptime(next_time_str, '%H:%M:%S')
            if zespol in df_przystanki['zespol'].values and slupek in df_przystanki['slupek'].values:
                # Pobieranie współrzędnych przystanku
                wspolrzedne_przystanku = get_coords(df_przystanki, zespol, slupek)

                # Pobieranie współrzędnych autobusu z pliku autobusy_i+1.json
                wspolrzedne_autobusu_2 = (row['Lat'], row['Lon'])

                # Pobieranie współrzędnych autobusu z pliku autobusy_i.json
                autobus_i_wiersz = df_1[(df_1['Lines'] == linia) & (df_1['Brigade'] == brygada)].iloc[0]
                wspolrzedne_autobusu_1 = (autobus_i_wiersz['Lat'], autobus_i_wiersz['Lon'])
                lonA = float(wspolrzedne_przystanku[1])
                latA = float(wspolrzedne_przystanku[0])
                lonB = float(wspolrzedne_autobusu_1[1])
                latB = float(wspolrzedne_autobusu_1[0])
                # Obliczanie odległości między przystankiem a autobusami
                odleglosc_przystanek_autobus_1 = distance(lonA, latA, lonB, latB)
                odleglosc_przystanek_autobus_2 = distance(lonA, latA, wspolrzedne_autobusu_2[1], wspolrzedne_autobusu_2[0])

                # Sprawdzenie, czy autobus dojechał do przystanku
                if odleglosc_przystanek_autobus_1 > odleglosc_przystanek_autobus_2 and odleglosc_przystanek_autobus_2 > 50:
                    #print(f"Autobus nie dojechał jeszcze do przystanku.")
                    opoznienia[(linia, brygada)] = {
                        'next_time_str': next_time_str,
                        'slupek': slupek,
                        'zespol': zespol
                    }
                else:
                    #print(f"Autobus dojechał do przystanku.")
                    # Sprawdź, czy dla tego autobusu istnieje informacja o opóźnieniu
                    if (linia, brygada) in opoznienia:
                        godziny1, minuty1, sekundy1 = map(int, next_time_str.split(':'))
                        #next_time = datetime.strptime(next_time_str, '%H:%M:%S')
                        #czas = datetime.strptime(czas_str, '%H:%M:%S')
                        godziny2, minuty2, sekundy2 = map(int, czas_str.split(':'))
                        if next_time_str >= czas_str:
                            opoznienie_seconds = ceil(0)
                            opoznienie = str(timedelta(seconds=opoznienie_seconds))
                            opoznienia.pop((linia, brygada))
                            """wyniki_analizy.append({
                                'Linia': linia,
                                'Brygada': brygada,
                                'Opóźnienie': opoznienie,
                                'Czas Analizy': czas_str,
                                'Lon': lonA,
                                'Lat': latA
                            })"""
                        else:
                            # Oblicz opóźnienie względem nowego przystanku zaokrąglone w górę do pełnej minuty
                            opoznienie_seconds = ceil((godziny2 - godziny1)*3600 + (minuty2-minuty1)*60 + sekundy2-sekundy1)
                            opoznienie = str(timedelta(seconds=opoznienie_seconds))
                            #print(f"Autobus na linii {linia}, brygada {brygada} o czasie {czas_str} ma opóźnienie {opoznienie}")
                            wyniki_analizy.append({
                                'Linia': linia,
                                'Brygada': brygada,
                                'Opóźnienie': opoznienie,
                                'Czas Analizy': czas_str,
                                'Lon': lonA,
                                'Lat': latA
                            })
                        next_time_str, slupek, zespol = find_next_stop(df_rozklady, linia, brygada, next_time_str)
                        if next_time_str is not None:
                            #next_time = datetime.strptime(next_time_str, '%H:%M:%S')
                            if zespol in df_przystanki['zespol'].values and slupek in df_przystanki['slupek'].values:
                                # Pobieranie współrzędnych przystanku
                                wspolrzedne_przystanku = get_coords(df_przystanki, zespol, slupek)
                                opoznienia[(linia, brygada)] = {
                                    'next_time_str': next_time_str,
                                    'slupek': slupek,
                                    'zespol': zespol
                                }
            else:
                print(f"Nieprawidłowe wartości zespolu i slupka: {zespol}, {slupek}")

    df_1 = df_filtered_2

# Tworzenie ramki danych z wynikami analizy
df_wyniki_analizy = pd.DataFrame(wyniki_analizy)

# Nazwa folderu, gdzie będą zapisane wyniki
wyniki_folder = folder_name + "_results"

# Tworzenie ścieżki do pliku CSV w folderze foldername
csv_file_path = os.path.join(wyniki_folder, 'wyniki_analizy.csv')

# Zapisanie ramki danych do pliku CSV
df_wyniki_analizy.to_csv(csv_file_path, index=False)
