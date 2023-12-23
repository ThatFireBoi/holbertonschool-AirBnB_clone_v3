#!/usr/bin/python3
"""Unittest for amenity.py"""

import unittest
import json
from models import storage
from models.amenity import Amenity
from api.v1.app import app
from api.v1.views.amenities import *


class TestAmenities(unittest.TestCase):
    """Test cases for the amenities route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_amenities(self):
        """Tests for a 200 status code"""
        response = self.app.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        """Tests for a specific amenity"""
        amenity = Amenity(name="Pool")
        amenity.save()
        response = self.app.get(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_amenity(self):
        """Tests amenity deletion"""
        amenity = Amenity(name="Gym")
        amenity.save()
        response = self.app.delete(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)

    def test_create_amenity(self):
        """Tests amenity creation"""
        response = self.app.post('/api/v1/amenities', data=json.dumps(
            {"name": "Sauna"}), content_type='application/json')
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
