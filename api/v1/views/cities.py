#!/usr/bin/python3
"""renders city api view"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_func(state_id):
    """Return a list of all City objects
    """
    key = "{}.{}".format(models.state.State.__name__, state_id)
    state = models.storage.all().get(key)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        name = data.get('name')
        if name is None:
            abort(400, 'Missing name')
        data.update({'state_id': state_id})
        obj = models.city.City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city_func(city_id):
    """Returns a city object
    """
    city_dict = {}
    key = "{}.{}".format(models.city.City.__name__, city_id)
    city = models.storage.all().get(key)
    if city is None:
        abort(404)
    if request.method == 'GET':
        city_dict = city.to_dict()
    elif request.method == 'DELETE':
        city.delete()
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                continue
            if hasattr(city, key):
                setattr(city, key, value)
            city.save()
            city_dict = city.to_dict()
    return jsonify(city_dict), 200
