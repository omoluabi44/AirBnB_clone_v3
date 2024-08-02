#!/usr/bin/python3
""" Index file for the api"""
from flask import jsonify
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


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


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])
    return jsonify(num_objs)
