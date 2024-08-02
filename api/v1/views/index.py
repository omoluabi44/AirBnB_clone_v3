#!/usr/bin/python3
""" Index file for the api"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns a JSON response with the status of the
    API. The response contains a single key-value pair
    Parameters:
        None

    Returns:
        A JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})
