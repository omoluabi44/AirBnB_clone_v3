#!/usr/bin/python3
""" objects that handle all default RestFul API actions for places  """
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
# from flasgger.utils import swag_from

@app_views.route('/cities/<city_id>/places', methods=['GET'],
    strict_slashes=False)       
def get_places(city_id):
    """ Retrieves all places of a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)   
def get_place(place_id):
    """ Retrieves a place object by its ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)    
def delete_place(place_id):
    """ Deletes a Place object by its ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
    strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object and saves it to the database """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)   
def update_place(place_id):
    """ Updates a Place object and saves it to the database """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at","user_id", "city_id"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


