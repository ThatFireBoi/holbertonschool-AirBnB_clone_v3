#!/usr/bin/python3
"""Unittest for index.py"""

import unittest
import json
from models import storage
from api.v1.app import app
from api.v1.views.index import *


class TestIndex(unittest.TestCase):
    """Test cases for the index route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        """Tests for a 200 status code"""
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)

    def test_status_output(self):
        """Tests for correct output"""
        response = self.app.get('/api/v1/status')
        self.assertEqual(json.loads(response.data), {"status": "OK"})

    def test_stats(self):
        """Tests stats route"""
        response = self.app.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)

    def test_stats_output(self):
        """Tests stats output"""
        response = self.app.get('/api/v1/stats')
        expected = {"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)}
        self.assertEqual(json.loads(response.data), expected)


if __name__ == "__main__":
    unittest.main()
