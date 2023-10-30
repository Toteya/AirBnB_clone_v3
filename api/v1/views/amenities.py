#!/usr/bin/python3
"""
Handles amenity API actions
"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
