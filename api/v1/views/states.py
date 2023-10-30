#!/usr/bin/python3
"""renders states view"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
import models
import sys


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    """Return a list of all States
    """
    from api.v1.app import app
    if request.method == 'GET':
        states = []
        for obj in models.storage.all(models.state.State).values():
            states.append(obj.to_dict())
        return jsonify(states)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        name = data.get('name')
        if name is None:
            abort(400, 'Missing name')
        # print("DATA: {} {}".format(data, type(data)), file=sys.stderr)
        obj = models.state.State(**data)
        obj.save()
        return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_obj(state_id):
    """Returns a State object matching the given id
    """
    state_dict = {}
    key = f"State.{state_id}"
    state = models.storage.all().get(key)
    if state is None:
        abort(404)
    if request.method == 'GET':
        state_dict = state.to_dict()
    elif request.method == 'DELETE':
        state.delete()
    elif request.method == 'PUT':

        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(state, key, value)
            state.save()
            state_dict = state.to_dict()
    return jsonify(state_dict)
