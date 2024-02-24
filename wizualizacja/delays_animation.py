import pandas as pd
import sys
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import geopandas as gpd
from visualizer import load_data_from_folder
from csv_data_loader import load_boundary
import numpy as np

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python delays_animation.py nazwa_folderu")
    sys.exit(1)

# Wczytanie nazwy folderu z argumentów
folder_name = sys.argv[1]

# Wczytanie danych z folderu
data = load_data_from_folder(folder_name, "wyniki_analizy.csv", 2)

# Wczytaj granice Warszawy z pliku Shapefile lub GeoJSON
warsaw_boundary = load_boundary("warszawa-dzielnice.geojson")

# Sprawdzenie, czy udało się wczytać dane
if data.empty:
    print("Nie udało się wczytać danych. Sprawdź nazwę folderu.")
    sys.exit(1)

# Konwersja kolumny 'Czas Analizy' do formatu daty
data['Czas Analizy'] = pd.to_datetime(data['Czas Analizy'])

# Zaokrąglenie czasu analizy do najbliższej minuty
data['Czas Analizy'] = data['Czas Analizy'].dt.round('min')

# Unikalne minuty w danych
unique_minutes = sorted(data['Czas Analizy'].unique())

# Obliczenie opóźnienia w minutach
data['Opóźnienie'] = pd.to_timedelta(data['Opóźnienie'])
data['Opóźnienie_min'] = data['Opóźnienie'].dt.total_seconds() / 60

# Inicjalizacja wykresu
fig, ax = plt.subplots()
warsaw_boundary.plot(ax=ax, color='none', edgecolor='black')

# Inicjalizacja punktów
scatter = ax.scatter([], [], s=10, c='blue', alpha=0.5)

# Inicjalizacja tekstu czasu
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='black')

# Funkcja skalująca kolor na podstawie opóźnienia
def scale_color(delay):
    if delay < 0:
        return 'blue'  # Małe opóźnienia na niebiesko
    elif delay >= 10:
        return 'red'   # Opóźnienia co najmniej 10 minut na czerwono
    else:
        # Stopniowe przejście od niebieskiego do czerwonego dla opóźnień pomiędzy 0 a 10 minutami
        return (1 - delay / 10, 0, delay / 10)

# Funkcja aktualizacji animacji
def update(frame):
    current_time = unique_minutes[frame].strftime("%Y-%m-%d %H:%M:%S")
    subset = data[(data['Czas Analizy'] >= unique_minutes[frame]) & (data['Czas Analizy'] < unique_minutes[frame + 1])]
    scatter.set_offsets(subset[['Lon', 'Lat']])
    scatter.set_color([scale_color(delay) for delay in subset['Opóźnienie_min']])
    time_text.set_text(f'Czas: {current_time}')
    return scatter, time_text

# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=len(unique_minutes) - 1, interval=500, blit=True, repeat=False)

# Dodanie suwaka do przewijania animacji
axslider = plt.axes([0.1, 0.02, 0.65, 0.03])
slider = Slider(axslider, 'Frames', 0, len(unique_minutes) - 1, valinit=0, valstep=1)

# Funkcja obsługi zmiany wartości suwaka
def update_frame(val):
    frame = int(slider.val)
    ax.cla()
    warsaw_boundary.plot(ax=ax, color='none', edgecolor='black')
    subset = data[(data['Czas Analizy'] >= unique_minutes[frame]) & (data['Czas Analizy'] < unique_minutes[frame + 1])]
    scatter = ax.scatter(subset['Lon'], subset['Lat'], s=10, c=[scale_color(delay) for delay in subset['Opóźnienie_min']], alpha=0.5)
    time_text = ax.text(0.02, 0.95, f'Czas: {unique_minutes[frame].strftime("%Y-%m-%d %H:%M:%S")}', transform=ax.transAxes, fontsize=12, color='black')

# Dodanie funkcji obsługi zmiany wartości suwaka
slider.on_changed(update_frame)

plt.show()
