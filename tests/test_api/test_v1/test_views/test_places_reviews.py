#!/usr/bin/python3
"""Unittest for reviews.py"""

import unittest
import json
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.app import app
from api.v1.views.places_reviews import *


class TestPlaceReviews(unittest.TestCase):
    """Test cases for the places_reviews route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_reviews(self):
        """Tests for a 200 status code"""
        user = User(email="test@test.com", password="test")
        user.save()
        state = State(name="California")
        state.save()
        city = City(name="Los Angeles", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place")
        place.save()
        response = self.app.get(f'/api/v1/places/{place.id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_review(self):
        """Tests for a specific review"""
        user = User(email="test2@test.com", password="test")
        user.save()
        state = State(name="California")
        state.save()
        city = City(name="Los Angeles", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place 2")
        place.save()
        review = Review(user_id=user.id, place_id=place.id,
                        text="Great place!")
        review.save()
        response = self.app.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Tests review deletion"""
        user = User(email="test3@test.com", password="test")
        user.save()
        state = State(name="Nevada")
        state.save()
        city = City(name="Las Vegas", state_id=state.id)
        city.save()
        place = Place(user_id=user.id, city_id=city.id, name="My place 3")
        place.save()
        review = Review(user_id=user.id, place_id=place.id,
                        text="Not so great place!")
        review.save()
        response = self.app.delete(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
