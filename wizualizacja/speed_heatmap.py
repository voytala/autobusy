from csv_data_loader import load_boundary
from visualizer import plot_heatmap, load_data_from_folder
import sys

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python heatmap_generation.py nazwa_folderu")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]
data = load_data_from_folder(folder_name, "prędkości_50.csv", 1)

# Wczytaj granice Warszawy z pliku Shapefile lub GeoJSON
warsaw_boundary = load_boundary("warszawa-dzielnice.geojson")

# Wygeneruj wykres ciepłowodny
plot_heatmap(data, warsaw_boundary)
