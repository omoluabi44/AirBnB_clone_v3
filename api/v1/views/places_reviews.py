#!/usr/bin/python3
""" objects that handle all default RestFul API actions for places_reviews """
from models.review import Review
from models.place  import Place
from models.user  import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
    strict_slashes=False)
def get_place_reviews(place_id):
    """ Retrieves all reviews of a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(jsonify([review.to_dict() for review in place.reviews]))

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_place_reviews_id(review_id):
    """ Retrieves a review object by its ID """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return make_response(jsonify(review_id.to_dict()))
@app_views.route('/reviews/<review_id>', methods=['DELETE'],strict_slashes=False)
def delete_place_review(review_id):
    """ Deletes a Review object by its ID """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)
@app_views.route('/places/<place_id>/reviews',  methods=['POST'],strict_slashes=False)
def create_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
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
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data["place_id"] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_place_review(review_id):
    """ Updates a Review object and saves it to the database """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
