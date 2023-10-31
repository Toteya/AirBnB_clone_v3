#!/usr/bin/python3
"""Handles user API actions"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users_func():
    """Return a list of all Users
    """
    if request.method == 'GET':
        users = []
        for obj in models.storage.all(models.user.User).values():
            users.append(obj.to_dict())
        return jsonify(users)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('password') is None:
            abort(400, 'Missing password')
        if data.get('email') is None:
            abort(400, 'Missing email')
        obj = models.user.User(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_obj(user_id):
    """Returns a User object matching the given id
    """
    user_dict = {}
    key = "{}.{}".format(models.user.User.__name__, user_id)
    user = models.storage.all().get(key)
    if user is None:
        abort(404)
    if request.method == 'GET':
        user_dict = user.to_dict()
    elif request.method == 'DELETE':
        user.delete()
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                continue
            if hasattr(user, key):
                setattr(user, key, value)
            user.save()
            user_dict = user.to_dict()
    return jsonify(user_dict)
