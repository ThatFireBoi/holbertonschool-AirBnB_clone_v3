#!/usr/bin/python3
"""Unittest for place.py"""

import unittest
import json
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from api.v1.app import app
from api.v1.views.places import *


class TestPlaces(unittest.TestCase):
    """Test cases for the places route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_place(self):
        """Tests for a specific place"""
        user = User(email="test@test.com", password="test")
        user.save()
        state = State(name="California")
        state.save()
        city = City(name="Los Angeles", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place")
        place.save()
        response = self.app.get(f'/api/v1/places/{place.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_place(self):
        """Tests place deletion"""
        user = User(email="test2@test.com", password="test")
        user.save()
        state = State(name="Nevada")
        state.save()
        city = City(name="Las Vegas", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place 2")
        place.save()
        response = self.app.delete(f'/api/v1/places/{place.id}')
        self.assertEqual(response.status_code, 200)

    def test_create_place(self):
        """Tests place creation"""
        user = User(email="test3@test.com", password="test")
        user.save()
        state = State(name="Oregon")
        state.save()
        city = City(name="Portland", state_id=state.id)
        city.save()
        response = self.app.post(
            f'/api/v1/cities/{city.id}/places',
            data=json.dumps({"user_id": user.id, "name": "My place 3"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_place(self):
        """Tests place update"""
        user = User(email="test4@test.com", password="test")
        user.save()
        state = State(name="Washington")
        state.save()
        city = City(name="Seattle", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place 4")
        place.save()
        response = self.app.put(f'/api/v1/places/{place.id}', data=json.dumps(
            {"name": "New place"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
