#!/usr/bin/python3
"""Handle reviews API actions"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_func(place_id):
    """Return a list of all Reviews
    """
    key = f"Place.{place_id}"
    place = models.storage.all().get(key)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = []
        for obj in place.reviews:
            reviews.append(obj.to_dict())
        return jsonify(reviews)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')
        if data.get('text') is None:
            abort(400, 'Missing text')
        data.update({'place_id': place_id})
        obj = models.review.Review(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_obj(review_id):
    """Returns a Review object matching the given id
    """
    review_dict = {}
    key = f"Review.{review_id}"
    review = models.storage.all().get(key)
    if review is None:
        abort(404)
    if request.method == 'GET':
        review_dict = review.to_dict()
    elif request.method == 'DELETE':
        review.delete()
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                continue
            setattr(review, key, value)
            review.save()
            review_dict = review.to_dict()
    return jsonify(review_dict), 200
