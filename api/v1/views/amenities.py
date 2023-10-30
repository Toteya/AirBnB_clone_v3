#!/usr/bin/python3
"""
Handles amenity API actions
"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities_func():
    if request.method == 'GET':
        amenities = []
        for obj in models.storage.all(models.amenities.Amenity).values():
            amenities.append(obj.to_dict())
        return jsonify(amenities)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        obj = models.amenity.Amenity(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE'])
def amenity_func(amenity_id):
    amenity_dict = {}
    key = f"Amenity.{amenity_id}"
    amenity = models.storage.all().get(key)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        amenity_dict = amenity.to_dict()
    elif request.method == 'DELETE':
        amenity.delete()
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(amenity, key, value)
            amenity.save()
            amenity_dict = amenity.to_dict()
    return jsonify(amenity_dict())
