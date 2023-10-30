#!/usr/bin/python3
"""
A flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """ calls method close """
    storage.close()


@app.errorhandler(404)
def page_not_found(error=None):
    """ returns a json formatted '404' status """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST")
    if host is None:
        host = "0.0.0.0"
    port = os.environ.get("HBNB_API_PORT")
    if port is None:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
