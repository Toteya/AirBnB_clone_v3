#!/usr/bin/python3
"""Handle places API actions"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/places_search', strict_slashes=False,
                 methods=['POST'])
def places_search_func():
    """Return a list of Places
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    states = data.get('states')
    cities = data.get('cities')
    amenities = data.get('amenities')

    places_list = []
    if not any([data, states, cities, amenities]):
        places = models.storage.all(models.place.Place).values()
        for obj in places:
            places_list.append(obj.to_dict())
        return jsoniify(places_list)

    city_list = []
    for state_id in states:
        key = "States.{}".format(state_id)
        state = models.storage.all().get(key)
        if state is None:
            continue
        for city in state.cities:
            city_list.append(city)
            # for place in city.places:
            #     places_list.append(place)

    for city_id in cities:
        key = "City.{}".format(city_id)
        city = models.storage.all().get(key)
        if city is None:
            continue
        if city not in city_list:
            city_list.append(city)

    for city in city_list:
        for place in city.places:
            places_list.append(place)
            print("HERE!!!: {}".format(place), file=sys.stderr)

    if amenities:
        filtered_place_list = places_list.copy()
        for place in places_list:
            place_amenity_ids = [amenity.id for amenity in place.amenities]
            if not all(a in place_amenity_ids for a in amenities):
                filtered_place_list.remove(place)
        places_list = filtered_place_list

    places_list = to_dict_list(places_list)
    return jsonify(places_list)


def to_dict_list(obj_list):
    """Converts a list of objects to a list of dicts
    """
    dict_list = []
    for obj in obj_list:
        dict_list.append(obj.to_dict())
    return dict_list
