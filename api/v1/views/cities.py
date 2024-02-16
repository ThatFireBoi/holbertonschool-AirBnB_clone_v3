#!/usr/bin/python3
"""City objects that handles all default RestFul API actions"""

# import the necessary modules
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


# Define route to return JSON of all City objects
@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns JSON of all City objects"""
    # Get the State object with the given id
    state = storage.get("State", state_id)
    # If no State object with that id exists, raise a 404 error
    if state is None:
        abort(404)
    # Create a list of all City objects in the State object
    cities = [city.to_dict() for city in state.cities]
    # Return a JSON response with the list
    return jsonify(cities)


# Define route to return JSON of a City object
@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns JSON of a City object"""
    # Get the City object with the given id
    city = storage.get("City", city_id)
    # If no City object with that id exists, raise a 404 error
    if city is None:
        abort(404)
    # Return a JSON response with the City object
    return jsonify(city.to_dict())


# Define route to delete a City object
@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    # Get the City object with the given id
    city = storage.get("City", city_id)
    # If no City object with that id exists, raise a 404 error
    if city is None:
        abort(404)
    # Delete the City object
    storage.delete(city)
    # Commit the change
    storage.save()
    # Return an empty JSON response with status code 200
    return jsonify({}), 200


# Define route to create a City object
@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
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
    # If the JSON does not contain a name key, raise a 400 error with a message
    if "name" not in json:
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    # Create a new City object with the name and the state_id
    city = City(**json)
    city.state_id = state_id
    # Save the new City object
    storage.new(city)
    # Commit the change
    storage.save()
    # Return a JSON response with the new City object and status code 201
    return jsonify(city.to_dict()), 201


# Define route to update a City object
@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
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
    # Update the City object with the JSON information
    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    # Save the updated City object
    storage.save()
    # Return a JSON response with the City object and status code 200
    return jsonify(city.to_dict()), 200
