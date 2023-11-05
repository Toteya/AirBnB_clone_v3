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

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities')

    places_list = []
    if not any([data, states, cities, amenities]):
        places = models.storage.all(models.place.Place).values()
        for obj in places:
            places_list.append(obj.to_dict())
        return jsonify(places_list)

    city_list = []
    for state_id in states:
        state = models.storage.get(models.state.State, state_id)
        if state is None:
            continue
        for city in state.cities:
            city_list.append(city)

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

    if amenities:
        if not any([states, cities]):
            places_list = list(models.storage.all(models.place.Place).values())
        place_ids = []
        for place in places_list:
            amenity_ids = [amenity.id for amenity in place.amenities]
            if all(a in amenity_ids for a in amenities):
                place_ids.append(place.id)
        models.storage.close()
        places_list = []
        places = models.storage.all(models.place.Place).values()
        for place in places:
            if place.id in place_ids:
                places_list.append(place)

    places_list = to_dict_list(places_list)
    return jsonify(places_list)


def to_dict_list(obj_list):
    """Converts a list of objects to a list of dicts
    """
    dict_list = []
    for obj in obj_list:
        dict_list.append(obj.to_dict())
    return dict_list
