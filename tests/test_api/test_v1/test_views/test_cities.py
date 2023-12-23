#!/usr/bin/python3
"""Unittest for city.py"""

import unittest
import json
from models import storage
from models.state import State
from models.city import City
from api.v1.app import app
from api.v1.views.cities import *


class TestCities(unittest.TestCase):
    """Test cases for the cities route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_cities(self):
        """Tests for a 200 status code"""
        state = State(name="California")
        state.save()
        response = self.app.get(f'/api/v1/states/{state.id}/cities')
        self.assertEqual(response.status_code, 200)

    def test_get_city(self):
        """Tests for a specific city"""
        state = State(name="California")
        state.save()
        city = City(name="Los Angeles", state_id=state.id)
        city.save()
        response = self.app.get(f'/api/v1/cities/{city.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_city(self):
        """Tests city deletion"""
        state = State(name="Nevada")
        state.save()
        city = City(name="Las Vegas", state_id=state.id)
        city.save()
        response = self.app.delete(f'/api/v1/cities/{city.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_city(self):
        """Tests city update"""
        state = State(name="Washington")
        state.save()
        city = City(name="Seattle", state_id=state.id)
        city.save()
        response = self.app.put(f'/api/v1/cities/{city.id}', data=json.dumps(
                                {"name": "New Seattle"}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
