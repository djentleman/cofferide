from shapely.geometry import LineString
import polyline
import json
from flask import request, Flask
from flask_cors import CORS, cross_origin
from data.poi.preprocessor import target_categories
from data_handler import fetch_data
from helpers import meters_to_lat_lng, lat_lng_to_meters, icons, pluralize, depluralize

app = Flask(__name__)
CORS(app, support_credentials=True)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

gdf = fetch_data()


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
