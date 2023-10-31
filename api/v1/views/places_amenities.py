#!/usr/bin/python3
"""Handle amenities API actions"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def place_amenities_func(place_id, amenity_id=None):
    """Handles API actions relating to place amenities
    """
    key = "Place.{}".format(place_id)
    place = models.storage.all().get(key)
    if place is None:
        abort(404)
    if request.method == 'GET':
        amenities = list_amenities(place)
        return jsonify(amenities)
    if request.method == 'DELETE':
        delete_amenity(place, amenity_id)
        return jsonify({})
    if request.method == 'POST':
        return link_amenity(place, amenity_id)


def list_amenities(place):
    """Returns a list of amenities of a place depending on the storage type
    For db_storage a list of Amenity objects, otherwise a list of Amenity IDs
    """
    amenities = []
    if models.storage_t == 'db':
        for obj in place.amenities:
            amenities.append(obj.to_dict())
    else:
        for id in place.amenity_ids:
            amenities.append(id)
    return amenities


def delete_amenity(place, amenity_id):
    """Deletes an amenity of a place
    """
    key = "Amenity.{}".format(amenity_id)
    amenity = models.storage.all().get(key)
    if amenity is None:
        abort(404)
    if models.storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        place.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        place.save()


def link_amenity(place, amenity_id):
    """Links an amenity to a place"""
    key = "Amenity.{}".format(amenity_id)
    amenity = models.storage.all().get(key)
    if amenity is None:
        abort(404)
    if models.storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity_id), 200
        place.amenity_ids.append(amenity_id)
        place.save()
        return jsonify(amenity_id), 201
