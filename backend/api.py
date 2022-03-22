from shapely.geometry import LineString
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
