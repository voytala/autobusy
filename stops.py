import os
import pandas as pd
from datetime import datetime
import numpy as np
import json
from filter import speed, distance, filter_data

def calculate_speed(dfA, dfB, fout_slow_speed):
    # Scal ramki danych dfA i dfB względem kolumny "VehicleNumber"
    merged_df = pd.merge(dfA, dfB, on="VehicleNumber", suffixes=('_A', '_B'))
    
    for _, row in merged_df.iterrows():
        dist = distance(row['Lon_A'], row['Lat_A'], row['Lon_B'], row['Lat_B'])
        sp = speed(dist, row['Time_A'], row['Time_B'])
        
        if sp < 5:  # Sprawdź, czy prędkość jest mniejsza niż 5 km/h
            fout_slow_speed.write(f"{row['VehicleNumber']};{row['Lon_A']};{row['Lat_A']};{row['Time_A']};{row['Lon_B']};{row['Lat_B']};{row['Time_B']};{dist};{sp}\n")

def analyze_data(folder_name):
    output_folder = folder_name + "_results"
    os.makedirs(output_folder, exist_ok=True)
    fout_slow_speed_path = os.path.join(output_folder, "wolne_ruchy.csv")
    
    fout_slow_speed = open(fout_slow_speed_path, 'wt')
    fout_slow_speed.write("VehicleNumber;LonA;LatA;TimeA;LonB;LatB;TimeB;Distance;Speed\n")
    
    file_list = os.listdir(folder_name)
    file_list.sort()  # Sortuj pliki według nazw
    
    for i in range(0, len(file_list) - 2, 3):  # Sprawdzamy co 3 migawkę
        print(f"Migawka {i}")
        fnameA = os.path.join(folder_name, file_list[i])
        dataA = filter_data(fnameA)

        fnameB = os.path.join(folder_name, file_list[i + 1])
        dataB = filter_data(fnameB)

        calculate_speed(dataA, dataB, fout_slow_speed)

    fout_slow_speed.close()

if __name__ == "__main__":
    folder_name = input("Podaj nazwę folderu z danymi: ")
    analyze_data(folder_name)
