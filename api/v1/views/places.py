#!/usr/bin/python3
"""Handle places API actions"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_func(city_id):
    """Return a list of all Places
    """
    key = f"City.{city_id}"
    city = models.storage.all().get(key)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = []
        for obj in city.places:
            places.append(obj.to_dict())
        return jsonify(places)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')
        if data.get('name') is None:
            abort(400, 'Missing name')
        # print("DATA: {} {}".format(data, type(data)), file=sys.stderr)
        data.update({'city_id': city_id})
        obj = models.place.Place(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_obj(place_id):
    """Returns a Place object matching the given id
    """
    place_dict = {}
    key = f"Place.{place_id}"
    place = models.storage.all().get(key)
    if place is None:
        abort(404)
    if request.method == 'GET':
        place_dict = place.to_dict()
    elif request.method == 'DELETE':
        place.delete()
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            setattr(place, key, value)
            place.save()
            place_dict = place.to_dict()
    return jsonify(place_dict), 200
