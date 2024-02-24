import seaborn as sns
import matplotlib.pyplot as plt
from map_config import warsaw_lon_min, warsaw_lon_max, warsaw_lat_min, warsaw_lat_max
import os
import pandas as pd
import inspect


def plot_scatter(data, boundary):
    plt.figure(figsize=(10, 6))
    ax = plt.axes()
    ax.set_xlim(warsaw_lon_min, warsaw_lon_max)
    ax.set_ylim(warsaw_lat_min, warsaw_lat_max)
    boundary.plot(ax=ax, color='none', edgecolor='black')
    sns.scatterplot(data=data, x='LonA', y='LatA', color='red', alpha=0.7, s=10, ax=ax)
    plt.title('Mapa zaznaczająca miejsca z przekroczeniem prędkości')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')
    plt.show()


def plot_heatmap(data, boundary):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(x=data['LonA'], y=data['LatA'], cmap="YlOrRd", fill=True, bw_method=0.05)
    plt.title('Skupienia przekraczania prędkości')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')
    boundary.plot(ax=plt.gca(), color='none', edgecolor='black')
    plt.xlim(warsaw_lon_min, warsaw_lon_max)
    plt.ylim(warsaw_lat_min, warsaw_lat_max)
    plt.show()


def load_data_from_folder(folder_name, file_name, delimiter):
    # Ścieżka do katalogu, w którym znajduje się bieżący skrypt
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    # Ścieżka do katalogu z danymi (folder_name) w katalogu głównym projektu
    folder_path = os.path.join(current_dir, os.pardir, folder_name + "_results")

    if not os.path.exists(folder_path):
        print(f"Katalog {folder_name}_results nie istnieje.")
        return pd.DataFrame()

    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        if delimiter == 1:
            return pd.read_csv(file_path, delimiter=';')
        if delimiter == 2:
            return pd.read_csv(file_path, delimiter=',')
    else:
        print(f"Plik {file_name} nie istnieje w folderze {folder_name}_results.")
        return pd.DataFrame()
