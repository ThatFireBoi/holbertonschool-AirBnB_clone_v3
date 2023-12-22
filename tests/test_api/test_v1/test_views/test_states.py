#!/usr/bin/python3
"""Unittest for state.py"""

import unittest
from models.state import State
import json
from models import storage
from api.v1.app import app
from api.v1.views import *


class TestState(unittest.TestCase):
    """Test cases for state.py"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_states(self):
        """Tests the GET method on /states"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Get the JSON response
        response = self.app.get('/api/v1/states')
        # Convert the JSON response to a dictionary
        response_dict = json.loads(response.data.decode('utf-8'))
        # Get the State object from the database
        state = storage.get("State", state.id)
        # Convert the State object to a dictionary
        state_dict = state.to_dict()
        # Test if the response dictionary is equal to the State dictionary
        self.assertEqual(response_dict, [state_dict])

    def test_get_state(self):
        """Tests the GET method on /states/<state_id>"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Get the JSON response
        response = self.app.get('/api/v1/states/{}'.format(state.id))
        # Convert the JSON response to a dictionary
        response_dict = json.loads(response.data.decode('utf-8'))
        # Get the State object from the database
        state = storage.get("State", state.id)
        # Convert the State object to a dictionary
        state_dict = state.to_dict()
        # Test if the response dictionary is equal to the State dictionary
        self.assertEqual(response_dict, state_dict)

    def test_delete_state(self):
        """Tests the DELETE method on /states/<state_id>"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Delete the State object
        response = self.app.delete('/api/v1/states/{}'.format(state.id))
        # Get the State object from the database
        state = storage.get("State", state.id)
        # Test if the State object is None
        self.assertIsNone(state)

    def test_create_state(self):
        """Tests the POST method on /states"""
        # Create a dictionary containing the JSON request
        json = {"name": "California"}
        # Create a State object
        state = State(**json)
        # Get the JSON response
        response = self.app.post('/api/v1/states', data=json)
        # Convert the JSON response to a dictionary
        response_dict = json.loads(response.data.decode('utf-8'))
        # Get the State object from the database
        state = storage.get("State", state.id)
        # Convert the State object to a dictionary
        state_dict = state.to_dict()
        # Test if the response dictionary is equal to the State dictionary
        self.assertEqual(response_dict, state_dict)

    def test_create_state_no_json(self):
        """Tests the POST method on /states with no JSON"""
        # Create a dictionary containing the JSON request
        json = {}
        # Get the JSON response
        response = self.app.post('/api/v1/states', data=json)
        # Test if the status code is 400
        self.assertEqual(response.status_code, 400)

    def test_create_state_no_name(self):
        """Tests the POST method on /states with no name"""
        # Create a dictionary containing the JSON request
        json = {"name": ""}
        # Get the JSON response
        response = self.app.post('/api/v1/states', data=json)
        # Test if the status code is 400
        self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        """Tests the PUT method on /states/<state_id>"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Create a dictionary containing the JSON request
        json = {"name": "New York"}
        # Get the JSON response
        response = self.app.put(
            '/api/v1/states/{}'.format(state.id), data=json)
        # Convert the JSON response to a dictionary
        response_dict = json.loads(response.data.decode('utf-8'))
        # Get the State object from the database
        state = storage.get("State", state.id)
        # Convert the State object to a dictionary
        state_dict = state.to_dict()
        # Test if the response dictionary is equal to the State dictionary
        self.assertEqual(response_dict, state_dict)

    def test_update_state_no_json(self):
        """Tests the PUT method on /states/<state_id> with no JSON"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Create a dictionary containing the JSON request
        json = {}
        # Get the JSON response
        response = self.app.put(
            '/api/v1/states/{}'.format(state.id), data=json)
        # Test if the status code is 400
        self.assertEqual(response.status_code, 400)

    def test_update_state_no_name(self):
        """Tests the PUT method on /states/<state_id> with no name"""
        # Create a State object
        state = State(name="California")
        # Save the State object
        storage.new(state)
        storage.save()
        # Create a dictionary containing the JSON request
        json = {"name": ""}
        # Get the JSON response
        response = self.app.put(
            '/api/v1/states/{}'.format(state.id), data=json)
        # Test if the status code is 400
        self.assertEqual(response.status_code, 400)

    def test_update_state_no_state(self):
        """Tests the PUT method on /states/<state_id> with no State object"""
        # Create a dictionary containing the JSON request
        json = {"name": "New York"}
        # Get the JSON response
        response = self.app.put(
            '/api/v1/states/{}'.format("123456"), data=json)
        # Test if the status code is 404
        self.assertEqual(response.status_code, 404)

    def test_update_state_no_state_id(self):
        """Tests the PUT method on /states/<state_id> with no state_id"""
        # Create a dictionary containing the JSON request
        json = {"name": "New York"}
        # Get the JSON response
        response = self.app.put('/api/v1/states/{}'.format(""), data=json)
        # Test if the status code is 404
        self.assertEqual(response.status_code, 404)

    def test_update_state_invalid_state_id(self):
        """Tests the PUT method on /states/<state_id> with an invalid state_id"""
        # Create a dictionary containing the JSON request
        json = {"name": "New York"}
        # Get the JSON response
        response = self.app.put(
            '/api/v1/states/{}'.format("123456"), data=json)
        # Test if the status code is 404
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
