from csv_data_loader import load_boundary
from visualizer import plot_scatter, load_data_from_folder
import sys

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python scatter_plot_generation.py nazwa_folderu")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]
data = load_data_from_folder(folder_name, "prędkości_50.csv", 1)

# Wczytaj granice Warszawy z pliku Shapefile lub GeoJSON
warsaw_boundary = load_boundary("warszawa-dzielnice.geojson")

# Generuj wykres punktowy
plot_scatter(data, warsaw_boundary)
