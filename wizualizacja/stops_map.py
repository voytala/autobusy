import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import sys
import seaborn as sns
from csv_data_loader import load_boundary
from visualizer import load_data_from_folder
from visualizer import plot_scatter
import sys

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python scatter_plot_generation.py nazwa_folderu")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]

# Wczytaj dane z plików
data_slow_speed = load_data_from_folder(folder_name, "wolne_ruchy.csv", 1)
data_terminals = pd.read_csv('terminals.csv', delimiter=',')

# Konwersja kolumn z współrzędnymi na typ Point
data_slow_speed['geometry'] = data_slow_speed.apply(
    lambda x: Point(x['LonA'], x['LatA']),
    axis=1
)

data_terminals['geometry'] = data_terminals.apply(
    lambda x: Point(x['Dlug_geo'], x['Szer_geo']),
    axis=1
)

# Tworzenie ramki danych geopandas
gdf_slow_speed = gpd.GeoDataFrame(data_slow_speed, geometry='geometry')
gdf_terminals = gpd.GeoDataFrame(data_terminals, geometry='geometry')

# Wczytanie granic Warszawy z pliku GeoJSON lub Shapefile
warsaw_boundary = gpd.read_file('warszawa-dzielnice.geojson')

# Utworzenie wykresu
fig, ax = plt.subplots(figsize=(10, 8))

# Narysowanie granic Warszawy
warsaw_boundary.plot(ax=ax, color='lightgray', edgecolor='black')

# Nanieś punkty z wolnych ruchów na czerwono
gdf_slow_speed.plot(ax=ax, color='red', label='Postój', markersize=5)

# Nanieś punkty z terminali na niebiesko
gdf_terminals.plot(ax=ax, color='blue', label='Terminal', markersize=50, alpha=0.5)

# Dodaj tytuł i etykiety osi
plt.title('Wizualizacja punktów postoju z mapą Warszawy')
plt.xlabel('Długość geograficzna')
plt.ylabel('Szerokość geograficzna')

# Dodaj legendę
plt.legend()

# Wyświetl wykres
plt.show()
