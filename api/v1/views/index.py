#!/usr/bin/python3
""" index module """

from api.v1.views import app_views
from flask import Flask, jsonify
import models


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns status in JSON format """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each object
    """
    obj_dict = {
            "amenities": models.storage.count(models.amenity.Amenity),
            "cities": models.storage.count(models.city.City),
            "places": models.storage.count(models.place.Place),
            "reviews": models.storage.count(models.review.Review),
            "states": models.storage.count(models.state.State),
            "users": models.storage.count(models.user.User)
        }
    return jsonify(obj_dict)
