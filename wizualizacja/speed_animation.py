import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
from map_config import warsaw_lon_min, warsaw_lon_max, warsaw_lat_min, warsaw_lat_max
from csv_data_loader import load_boundary
from visualizer import load_data_from_folder
import sys

# Wczytaj granice Warszawy z pliku Shapefile lub GeoJSON
warsaw_boundary = load_boundary("warszawa-dzielnice.geojson")

# Sprawdzenie, czy podano nazwę folderu jako argument
if len(sys.argv) != 2:
    print("Użycie: python delays_animation.py nazwa_folderu")
    sys.exit(1)

# Wczytaj dane z odpowiedniego pliku i folderu
folder_name = sys.argv[1]
data = load_data_from_folder(folder_name, "prędkości_50.csv", 1)
data['TimeA'] = pd.to_datetime(data['TimeA'])

# Posortuj dane według czasu
data.sort_values(by='TimeA', inplace=True)

# Inicjalizacja wykresu
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(warsaw_lon_min, warsaw_lon_max)
ax.set_ylim(warsaw_lat_min, warsaw_lat_max)
warsaw_boundary.plot(ax=ax, color='none', edgecolor='black')

# Inicjalizacja punktów
scatter = ax.scatter([], [], s=10, c='red', alpha=0.5)

# Inicjalizacja tekstu czasu
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='black')


# Funkcja aktualizacji animacji
def update(frame):
    current_time = data.iloc[frame]['TimeA'].strftime("%Y-%m-%d %H:%M:%S")
    subset = data.iloc[:frame+1]
    scatter.set_offsets(subset[['LonA', 'LatA']])
    time_text.set_text(f'Czas: {current_time}')
    return scatter, time_text


# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=len(data), interval=100, blit=True, repeat=False)

# Definiowanie przycisków
axprev = plt.axes([0.81, 0.05, 0.1, 0.04])
axnext = plt.axes([0.93, 0.05, 0.1, 0.04])
axslider = plt.axes([0.1, 0.02, 0.65, 0.03])

bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Previous')
slider = Slider(axslider, 'Frames', 0, len(data) - 1, valinit=0, valstep=1)


# Funkcje obsługi zdarzeń przycisków i suwaka
def nextframe(event):
    slider.set_val(min(slider.val + 1, len(data) - 1))


def prevframe(event):
    slider.set_val(max(slider.val - 1, 0))


def updateframe(val):
    frame = int(slider.val)
    ax.cla()
    ax.set_xlim(warsaw_lon_min, warsaw_lon_max)
    ax.set_ylim(warsaw_lat_min, warsaw_lat_max)
    warsaw_boundary.plot(ax=ax, color='none', edgecolor='black')
    subset = data.iloc[:frame+1]
    scatter = ax.scatter(subset['LonA'], subset['LatA'], s=10, c='red', alpha=0.5)
    last_time = subset.iloc[-1]["TimeA"].strftime("%Y-%m-%d %H:%M:%S")
    time_text = ax.text(
        0.02,
        0.95,
        f'Czas: {last_time}',
        transform=ax.transAxes,
        fontsize=12,
        color='black'
    )
    ax.set_title('Mapa zaznaczająca miejsca z przekroczeniem prędkości')


bnext.on_clicked(nextframe)
bprev.on_clicked(prevframe)
slider.on_changed(updateframe)

plt.show()
