import pandas as pd
import sys
from visualizer import load_data_from_folder

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 4:
    print("Użycie: python delay_list.py nazwa_folderu linia brygada")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]
line = sys.argv[2]
brigade = str(sys.argv[3])
data = load_data_from_folder(folder_name, "wyniki_analizy.csv", 2)

# Wybierz opóźnienia dla określonej linii i brygady
selected_delays = data[(data['Linia'] == line) & (data['Brygada'] == brigade)]

# Posortuj opóźnienia po czasie
selected_delays_sorted = selected_delays.sort_values(by='Czas Analizy')

# Wyświetl posortowaną listę opóźnień
print(selected_delays_sorted)
