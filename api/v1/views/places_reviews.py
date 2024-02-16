#!/usr/bin/python3
"""Places_Reviews objects that handles all default RestFul API actions"""

# import the necessary modules
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


# Define route to return JSON of all Review objects
@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns JSON of all Review objects"""
    # Get the Place object with the given id
    place = storage.get("Place", place_id)
    # If no Place object with that id exists, raise a 404 error
    if place is None:
        abort(404)
    # Create a list of all Review objects in the Place object
    reviews = [review.to_dict() for review in place.reviews]
    # Return a JSON response with the list
    return jsonify(reviews)


# Define route to return JSON of a Review object
@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns JSON of a Review object"""
    # Get the Review object with the given id
    review = storage.get("Review", review_id)
    # If no Review object with that id exists, raise a 404 error
    if review is None:
        abort(404)
    # Return a JSON response with the Review object
    return jsonify(review.to_dict())


# Define route to delete a Review object
@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    # Get the Review object with the given id
    review = storage.get("Review", review_id)
    # If no Review object with that id exists, raise a 404 error
    if review is None:
        abort(404)
    # Delete the Review object
    storage.delete(review)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a Review object
@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    # Get the Place object with the given id
    place = storage.get("Place", place_id)
    # If no Place object with that id exists, raise a 404 error
    if place is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "user_id" not in json:
        abort(make_response(jsonify({"error": "Missing user_id"}), 400))
    # Get the User object with the given id
    user = storage.get("User", json["user_id"])
    # If no User object with that id exists, raise a 404 error
    if user is None:
        abort(404)
    # If the JSON does not contain a text key, raise a 400 error with a message
    if "text" not in json:
        abort(make_response(jsonify({"error": "Missing text"}), 400))
    # Add the Place id to the JSON
    json["place_id"] = place_id
    # Create the Review object
    review = Review(**json)
    # Save the Review object
    storage.new(review)
    # Commit the change
    storage.save()
    # Return a JSON response with the new Review object
    return jsonify(review.to_dict()), 201


# Define route to update a Review object
@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    # Get the Review object with the given id
    review = storage.get("Review", review_id)
    # If no Review object with that id exists, raise a 404 error
    if review is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # Update the Review object
    for key, value in json.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    # Save the Review object
    storage.save()
    # Return a JSON response with the Review object
    return jsonify(review.to_dict()), 200
