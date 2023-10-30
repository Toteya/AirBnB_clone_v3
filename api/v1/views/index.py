#!/usr/bin/python3
""" index module """

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns status in JSON format """
    return jsonify({"status": "OK"})
