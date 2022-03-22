
# very bad code
# a wise man once said: "Don't try to do any analysis in Alaska"
meters_to_lat_lng = lambda x: x*111132.954
lat_lng_to_meters = lambda x: x/111132.954

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

def transponse(x):
    return list(map(lambda x: [x[1], x[0]], x))
