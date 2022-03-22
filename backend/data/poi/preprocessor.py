from shapely.geometry import shape
import sys
import geopandas
import geojson

target_categories = ['restaurant', 'cafe', 'fast_food', 'convenience', 'toilets', 'place_of_worship']

def preprocess_feature(f):
    prop = f['properties']
    # useful https://wiki.openstreetmap.org/wiki/Map_features
    if 'shop' in prop.keys():
        cat_col = 'shop'
    elif 'amenity' in prop.keys():
        cat_col = 'amenity'
    else:
        return None
    name_col = 'name_en' if 'name:en' in prop.keys() else 'name'
    return {
        'fid': f['properties']['@id'],
        'name': f['properties'].get(name_col),
        'geometry': shape(f['geometry']).centroid, # easier to compute with centroid
        'high_level_category': cat_col,
        'category': f['properties'].get(cat_col),
        'known_bike_parking': f['properties'].get('bicycle_parking', False)
    }

def preprocess_series(series):
    fname = f'raw_data/{series}.geojson'
    with open(fname) as f:
        gj = geojson.load(f)
    features = gj['features']
    preprocessed_poi = [preprocess_feature(f) for f in features]
    preprocessed_poi = [p for p in preprocessed_poi if p is not None]
    gdf = geopandas.GeoDataFrame(preprocessed_poi)
    gdf = gdf[~gdf.name.isna()]
    output_dir = f'processed_data/{series}.geojson'
    gdf.to_file(output_dir, driver="GeoJSON")

def main():
    series = sys.argv[1]
    assert series in target_categories
    gdf = preprocess_series(series)

if __name__ == '__main__':
    main()
