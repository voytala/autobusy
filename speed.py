import os
import pandas as pd
from speed_common import speed, distance, filter_data


def calculate_speed(dfA, dfB, fout, fout50):
    # Scal ramki danych dfA i dfB względem kolumny "VehicleNumber"
    merged_df = pd.merge(dfA, dfB, on="VehicleNumber", suffixes=('_A', '_B'))

    for _, row in merged_df.iterrows():
        dist = distance(row['Lon_A'], row['Lat_A'], row['Lon_B'], row['Lat_B'])
        sp = speed(dist, row['Time_A'], row['Time_B'])

        fout.write(
            f"{row['VehicleNumber']};{row['Lon_A']};{row['Lat_A']};"
            f"{row['Time_A']};{row['Lon_B']};{row['Lat_B']};"
            f"{row['Time_B']};{dist};{sp}\n"
        )

        if sp > 50:
            fout50.write(
                f"{row['VehicleNumber']};{row['Lon_A']};{row['Lat_A']};"
                f"{row['Time_A']};{row['Lon_B']};{row['Lat_B']};"
                f"{row['Time_B']};{dist};{sp}\n"
            )


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
