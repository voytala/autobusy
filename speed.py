import os
import pandas as pd
from datetime import datetime
import math
import numpy as np
import json

def calculate_speed(dfA, dfB, fout, fout50):
    # Scal ramki danych dfA i dfB względem kolumny "VehicleNumber"
    merged_df = pd.merge(dfA, dfB, on="VehicleNumber", suffixes=('_A', '_B'))
    
    for _, row in merged_df.iterrows():
        dist = distance(row['Lon_A'], row['Lat_A'], row['Lon_B'], row['Lat_B'])
        sp = speed(dist, row['Time_A'], row['Time_B'])
        
        fout.write(f"{row['VehicleNumber']};{row['Lon_A']};{row['Lat_A']};{row['Time_A']};{row['Lon_B']};{row['Lat_B']};{row['Time_B']};{dist};{sp}\n")
        
        if sp > 50:
            fout50.write(f"{row['VehicleNumber']};{row['Lon_A']};{row['Lat_A']};{row['Time_A']};{row['Lon_B']};{row['Lat_B']};{row['Time_B']};{dist};{sp}\n")

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

def analyze_data(folder_name):
    output_folder = folder_name + "_results"
    os.makedirs(output_folder, exist_ok=True)
    fout_path = os.path.join(output_folder, "prędkości.csv")
    fout50_path = os.path.join(output_folder, "prędkości_50.csv")
    
    fout = open(fout_path, 'wt')
    fout50 = open(fout50_path, 'wt')
    fout.write("VehicleNumber;LonA;LatA;TimeA;LonB;LatB;TimeB;Distance;Speed\n")
    fout50.write("VehicleNumber;LonA;LatA;TimeA;LonB;LatB;TimeB;Distance;Speed\n")
    
    file_list = os.listdir(folder_name)
    file_list.sort()  # Sortuj pliki według nazw
    
    for i in range(len(file_list) - 1):
        print(f"Migawka {i}")
        fnameA = os.path.join(folder_name, file_list[i])
        dataA = filter_data(fnameA)

        fnameB = os.path.join(folder_name, file_list[i + 1])
        dataB = filter_data(fnameB)

        calculate_speed(dataA, dataB, fout, fout50)

    fout50.close()
    fout.close()

if __name__ == "__main__":
    folder_name = input("Podaj nazwę folderu z danymi: ")
    analyze_data(folder_name)
