#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

# import the necessary modules
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


# Define route to return JSON of all Amenity objects
@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns JSON of all Amenity objects"""
    # Create a list of all Amenity objects
    amenities = [amenity.to_dict()
                 for amenity in storage.all("Amenity").values()]
    # Return a JSON response with the list
    return jsonify(amenities)


# Define route to return JSON of a Amenity object
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns JSON of a Amenity object"""
    # Get the Amenity object with the given id
    amenity = storage.get("Amenity", amenity_id)
    # If no Amenity object with that id exists, raise a 404 error
    if amenity is None:
        abort(404)
    # Return a JSON response with the Amenity object
    return jsonify(amenity.to_dict())


# Define route to delete a Amenity object
@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    # Get the Amenity object with the given id
    amenity = storage.get("Amenity", amenity_id)
    # If no Amenity object with that id exists, raise a 404 error
    if amenity is None:
        abort(404)
    # Delete the Amenity object
    storage.delete(amenity)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a Amenity object
@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "name" not in json:
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    # Create a new Amenity object with the name
    amenity = Amenity(**json)
    # Save the new Amenity object to the database
    amenity.save()
    # Return a JSON response with the new Amenity object and status code 201
    return jsonify(amenity.to_dict()), 201


# Define route to update a Amenity object
@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    # Get the Amenity object with the given id
    amenity = storage.get("Amenity", amenity_id)
    # If no Amenity object with that id exists, raise a 404 error
    if amenity is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # Update the Amenity object
    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    # Save the Amenity object to the database
    amenity.save()
    # Return a JSON response with the Amenity object and status code 200
    return jsonify(amenity.to_dict()), 200
