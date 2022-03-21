from shapely.geometry import shape, LineString
import geopandas
import geojson
import polyline
import json
from flask import request, Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


# very bad code
# a wise man once said: "Don't try to do any analysis in Alaska"
meters_to_lat_lng = lambda x: x*111132.954
lat_lng_to_meters = lambda x: x/111132.954

target_categories = ['restaurant', 'cafe', 'fast_food', 'convenience', 'toilets', 'place_of_worship']

icons = {
    'cafe': 'https://img.icons8.com/color/344/cafe--v1.png',
    'restaurant': 'https://img.icons8.com/color/344/dining-room.png',
    'convenience': 'https://img.icons8.com/color/344/grocery-store.png',
    'place_of_worship': 'https://img.icons8.com/color/344/torii.png',
    'toilets': 'https://img.icons8.com/color/344/toilet.png',
    'fast_food': 'https://img.icons8.com/color/344/hamburger.png'
}

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

# NOTE: this was a geojson export of OSM data
# TODO: replace it with properly curated data
with open('export.geojson') as f:
    gj = geojson.load(f)
features = gj['features']

preprocessed_poi = [preprocess_feature(f) for f in features]
preprocessed_poi = [p for p in preprocessed_poi if p is not None]
gdf = geopandas.GeoDataFrame(preprocessed_poi)
gdf = gdf[~gdf.name.isna()]
gdf = gdf[gdf.category.isin(target_categories)]


def pluralize(s):
    if s[-1] == s:
        return s
    return f'{s}s'

def depluralize(s):
    if s[-1] == s:
        return s[:-1]
    return s

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/get_poi')
@cross_origin(supports_credentials=True)
def get_poi():

    gpx = request.args.get('gpx')
    # decode
    coords = polyline.decode(gpx)
    ls = LineString(coords)
    area_of_interest = ls.buffer(lat_lng_to_meters(100))
    relevant_poi = gdf[gdf.intersects(area_of_interest)]

    payload = [
        {
            'series': pluralize(cat),
            'name': depluralize(cat),
            'source': json.loads(relevant_poi[relevant_poi.category == cat].to_json()),
            'icon': icons.get(cat)
        }
        for cat in target_categories
    ]

    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(port=5000,debug=True)
