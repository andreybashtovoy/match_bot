import googlemaps

from dtb.settings import PLACES_API_KEY

maps_api = googlemaps.Client(key=PLACES_API_KEY)


def search_place(name: str):
    place_search = maps_api.places(
        name
    )

    return place_search['results']


def get_place_name(lat, lng):
    results = maps_api.places(location=(lat, lng), type="cities")['results']

    if len(results):
        return results[0]['name']
    else:
        return "-"
