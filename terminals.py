import pandas as pd
import json
from speed_common import get_coords

# Tworzymy pustą listę, do której będziemy dodawać krotki z danymi
data_list = []

# Wczytujemy dane z pliku JSON
with open('schedules.json', 'r') as file:
    json_data = json.load(file)

# Przechodzimy przez dane JSON i dodajemy informacje o liniach, trasach i przystankach do listy
for linia, trasy in json_data['result'].items():
    for trasa, przystanki in trasy.items():
        for nr, info in przystanki.items():
            data_list.append((linia, trasa, int(nr), info['nr_zespolu'], info['nr_przystanku']))

# Tworzymy ramkę danych pandas na podstawie zebranych danych
df = pd.DataFrame(data_list, columns=['Linia', 'Trasa', 'Nr_Przystanku', 'Nr_Zespolu', 'Nr_slupka'])

# Wczytujemy dane o lokalizacji przystanków autobusowych
with open('przystanki.json', 'r') as f:
    data = json.load(f)

# Tworzymy pustą listę, do której będziemy dodawać słowniki z danymi o lokalizacji przystanków
rows = []

# Iterujemy przez wyniki z pliku JSON i dodajemy je do listy
for result in data['result']:
    values_dict = {}
    for value in result['values']:
        values_dict[value['key']] = value['value']
    rows.append(values_dict)

# Tworzymy ramkę danych pandas na podstawie zebranych danych o lokalizacji przystanków
df_przystanki = pd.DataFrame(rows)

# Resetujemy indeks ramki danych df_przystanki
df_przystanki.reset_index(drop=True, inplace=True)

# Grupujemy dane po liniach i trasach, znajdując minimalny i maksymalny numer przystanku
df_grouped = df.groupby(['Linia', 'Trasa']).agg({'Nr_Przystanku': ['min', 'max']}).reset_index()

# Łączymy dane na podstawie wartości min i max, aby uzyskać pełne informacje o wierszach
df_grouped.columns = ['Linia', 'Trasa', 'Nr_Przystanku_min', 'Nr_Przystanku_max']  # Zmiana nazw kolumn
df_filtered = pd.merge(df, df_grouped, on=['Linia', 'Trasa'])

df_filtered = df_filtered[
    (df_filtered['Nr_Przystanku'] == df_filtered['Nr_Przystanku_min']) |
    (df_filtered['Nr_Przystanku'] == df_filtered['Nr_Przystanku_max'])
]

# Usunięcie kolumny 'Trasa' z ramki danych df_filtered
df_filtered.drop(columns=['Trasa'], inplace=True)
df_filtered.drop(columns=['Nr_Przystanku'], inplace=True)
df_filtered.drop(columns=['Nr_Przystanku_min'], inplace=True)
df_filtered.drop(columns=['Nr_Przystanku_max'], inplace=True)

# Usunięcie duplikatów z ramki danych df_filtered
df_filtered.drop_duplicates(inplace=True)

# Iteracja po wierszach ramki danych df_filtered
for index, row in df_filtered.iterrows():
    # Pobranie numeru zespołu i numeru słupka
    zespol = row['Nr_Zespolu']
    slupek = row['Nr_slupka']

    # Pobranie współrzędnych dla danego przystanku
    szer_geo, dlug_geo = get_coords(df_przystanki, zespol, slupek)

    # Aktualizacja ramki danych df_filtered z uzyskanymi współrzędnymi
    df_filtered.at[index, 'Szer_geo'] = szer_geo
    df_filtered.at[index, 'Dlug_geo'] = dlug_geo

# Zapisanie ramki danych df_filtered do pliku CSV
df_filtered.to_csv('terminals.csv', index=False)
