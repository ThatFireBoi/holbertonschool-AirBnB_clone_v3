#!/usr/bin/python3
"""States view for api v1"""

# Import necessary modules and classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


# Define route to return JSON of all State objects
@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Returns JSON of all State objects"""
    # Create a list of all State objects
    states = [state.to_dict() for state in storage.all("State").values()]
    # Return a JSON response with the list
    return jsonify(states)


# Define route to return JSON of a State object
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns JSON of a State object"""
    # Get the State object with the given id
    state = storage.get("State", state_id)
    # If no State object with that id exists, raise a 404 error
    if state is None:
        abort(404)
    # Return a JSON response with the State object
    return jsonify(state.to_dict())


# Define route to delete a State object
@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    # Get the State object with the given id
    state = storage.get("State", state_id)
    # If no State object with that id exists, raise a 404 error
    if state is None:
        abort(404)
    # Delete the State object
    storage.delete(state)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a State object
@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "name" not in json:
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    # Create a new State object with the name
    state = State(**json)
    # Save the new State object
    storage.new(state)
    # Commit the change
    storage.save()
    # Return a JSON response with the new State object and status code 201
    return jsonify(state.to_dict()), 201


# Define route to update a State object
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    # Get the State object with the given id
    state = storage.get("State", state_id)
    # If no State object with that id exists, raise a 404 error
    if state is None:
        abort(404)
    # Get the JSON from the request
    json = request.get_json()
    # If no JSON was sent, raise a 400 error with a message
    if json is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    # Update the State object
    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    # Commit the change
    storage.save()
    # Return a JSON response with the State object and status code 200
    return jsonify(state.to_dict()), 200
