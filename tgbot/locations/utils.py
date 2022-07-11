import googlemaps

from dtb.settings import PLACES_API_KEY

maps_api = googlemaps.Client(key=PLACES_API_KEY)


def search_place(name: str):
    place_search = maps_api.places(
        name
    )

    return place_search['results']
