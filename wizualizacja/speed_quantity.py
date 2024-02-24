from visualizer import load_data_from_folder
import sys

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python count_unique_vehicles.py nazwa_folderu")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]
data = load_data_from_folder(folder_name, "prędkości_50.csv", 1)

# Wybierz unikalne numery autobusów, które przekroczyły prędkość
unique_vehicles = data['VehicleNumber'].unique()

# Zlicz liczbę różnych autobusów
result = len(unique_vehicles)

print(f"Liczba różnych autobusów, które przekroczyły prędkość: {result}")
