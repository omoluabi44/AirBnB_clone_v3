#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.review import Review
from models.place  import Place
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
def get_place_reviews(review_id):
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