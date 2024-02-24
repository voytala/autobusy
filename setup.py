from setuptools import setup, find_packages

setup(
    name='projekt_autobusy',
    version='0.1.0',
    description='Projekt zaliczeniowy na Kurs Programowania w Pythonie',
    author='Piotr Wojtala',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'geopandas',
        'shapely',
        'ijson',
        'geojson',
        'seaborn',
        'requests',
        'numpy'
    ],
)
