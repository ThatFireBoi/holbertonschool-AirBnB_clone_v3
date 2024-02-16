#!/usr/bin/python3
"""User objects that handles all default RestFul API actions"""

# import the necessary modules
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


# Define route to return JSON of all User objects
@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Returns JSON of all User objects"""
    # Create a list of all User objects
    users = [user.to_dict() for user in storage.all("User").values()]
    # Return a JSON response with the list
    return jsonify(users)


# Define route to return JSON of a User object
@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns JSON of a User object"""
    # Get the User object with the given id
    user = storage.get("User", user_id)
    # If no User object with that id exists, raise a 404 error
    if user is None:
        abort(404)
    # Return a JSON response with the User object
    return jsonify(user.to_dict())


# Define route to delete a User object
@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    # Get the User object with the given id
    user = storage.get("User", user_id)
    # If no User object with that id exists, raise a 404 error
    if user is None:
        abort(404)
    # Delete the User object
    storage.delete(user)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a User object
@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "email" not in json:
        abort(make_response(jsonify({"error": "Missing email"}), 400))
    if "password" not in json:
        abort(make_response(jsonify({"error": "Missing password"}), 400))
    # Create a new User object with the name
    user = User(**json)
    # Save the new User object to storage
    storage.new(user)
    # Commit the change
    storage.save()
    # Return a JSON response with the new User object and status code 201
    return jsonify(user.to_dict()), 201


# Define route to update a User object
@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    # Get the User object with the given id
    user = storage.get("User", user_id)
    # If no User object with that id exists, raise a 404 error
    if user is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # Update the User object
    for key, value in json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    # Save the updated User object
    storage.save()
    # Return a JSON response with the User object and status code 200
    return jsonify(user.to_dict()), 200
