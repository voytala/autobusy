import pandas as pd
import geopandas as gpd

def load_data(filename):
    return pd.read_csv(filename, sep=';')

def load_boundary(filename):
    return gpd.read_file(filename)
