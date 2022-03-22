from data.poi.preprocessor import target_categories
import geopandas
import pandas as pd
import geojson


def fetch_data():
    gdfs = []
    for cat in target_categories:
        fname = f'data/poi/processed_data/{cat}.geojson'
        print(f'loading {fname}...')
        gdf = geopandas.read_file(fname)
        gdfs.append(gdf)
    return pd.concat(gdfs)
    

