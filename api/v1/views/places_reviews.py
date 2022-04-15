#!/usr/bin/python3
"""
view for reivew objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


places = []
places_dict = storage.all(Place)
for k, v in places_dict.items():
    places.append(v.to_dict())

reviews = []
reviews_dict = storage.all(Review)
for k, v in reviews_dict.items():
    reviews.append(v.to_dict())

users = []
users_dict = storage.all(User)
for k, v in users_dict.items():
    users.append(v.to_dict())


@app_views.route('/places/<place_id>/reviews')
def get_places_review(place_id):
    nill = []
    """Retrieves the list of all places Review objects """
    place = [place for place in places if place['id'] == place_id]
    if len(place) == 0:
        abort(404)
    for review in reviews:
        if review['place_id'] == place_id:
            nill.append(review)
    return jsonify(nill)


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """"Retrieves a Review object"""
    review = [review for review in reviews if review['id'] == review_id]
    if len(review) == 0:
        abort(404)
    return jsonify(review[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review Object"""
    review = [review for review in reviews if review['id'] == review_id]
    if len(review) == 0:
        abort(404)
    reviews.remove(review[0])
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review(place_id):
    """creates a reviews"""
    place = [place for place in places if place['id'] == place_id]
    if len(place) == 0:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)
    user = [
        user for user in users if user['id'] == request.get_json()['user_id']
        ]
    if len(user) == 0:
        print("no user")
        abort(404)
    if 'text' not in request.get_json():
        return ("Missing text\n", 400)
    request_data = request.get_json()
    new_review = Review(text=request_data['text'],
                        place_id=place_id,
                        user_id=request.get_json()['user_id'])
    reviews.append(new_review.to_dict())
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates a review"""
    review = [review for review in reviews if review['id'] == review_id]
    if len(review) == 0:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('user_id', None)
    request_data.pop('place_id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    review[0].update(request_data)
    return jsonify(review[0]), 200