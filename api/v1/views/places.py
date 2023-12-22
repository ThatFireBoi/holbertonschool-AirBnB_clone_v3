#!/usr/bin/python3
"""Place objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


# Define route to return JSON of all Place objects
@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns JSON of all Place objects"""
    # Get the City object with the given id
    city = storage.get("City", city_id)
    # If no City object with that id exists, raise a 404 error
    if city is None:
        abort(404)
    # Create a list of all Place objects in the City object
    places = [place.to_dict() for place in city.places]
    # Return a JSON response with the list
    return jsonify(places)


# Define route to return JSON of a Place object
@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns JSON of a Place object"""
    # Get the Place object with the given id
    place = storage.get("Place", place_id)
    # If no Place object with that id exists, raise a 404 error
    if place is None:
        abort(404)
    # Return a JSON response with the Place object
    return jsonify(place.to_dict())


# Define route to delete a Place object
@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    # Get the Place object with the given id
    place = storage.get("Place", place_id)
    # If no Place object with that id exists, raise a 404 error
    if place is None:
        abort(404)
    # Delete the Place object
    storage.delete(place)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a Place object
@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    # Get the City object with the given id
    city = storage.get("City", city_id)
    # If no City object with that id exists, raise a 404 error
    if city is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # If the JSON does not contain a user_id key, raise a 400 error with a msg
    if "user_id" not in json:
        abort(make_response(jsonify({"error": "Missing user_id"}), 400))
    # Get the User object with the given user_id
    user = storage.get("User", json["user_id"])
    # If no User object with that id exists, raise a 404 error
    if user is None:
        abort(404)
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "name" not in json:
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    # Add the City id to the JSON
    json["city_id"] = city_id
    # Create a new Place object with the JSON
    place = Place(**json)
    # Save the new Place object
    place.save()
    # Return a JSON response with the new Place object and status code 201
    return jsonify(place.to_dict()), 201


# Define route to update a Place object
@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
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
    # Update the Place object
    for key, value in json.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    # Save the updated Place object
    place.save()
    # Return a JSON response with the updated Place object and status code 200
    return jsonify(place.to_dict()), 200
