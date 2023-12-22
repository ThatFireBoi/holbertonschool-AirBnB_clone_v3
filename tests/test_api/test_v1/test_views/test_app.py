#!/usr/bin/python3
"""Unittest for app.py"""

import unittest
from flask import Flask
from api.v1.app import app
from flask_cors import CORS


class TestApp(unittest.TestCase):
    """Test cases for the app"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_app_creation(self):
        """Tests if the app is created successfully"""
        self.assertIsInstance(app, Flask)


class TestCORS(unittest.TestCase):
    """Test cases for CORS"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_cors_headers(self):
        """Tests if CORS headers are set"""
        response = self.app.get('/')
        self.assertIn('Access-Control-Allow-Origin', response.headers)

    def test_cors_origin(self):
        """Tests if CORS headers are set"""
        response = self.app.get('/')
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_cors_methods(self):
        """Tests if CORS headers are set"""
        response = self.app.get('/')
        self.assertIn('Access-Control-Allow-Methods', response.headers)


if __name__ == "__main__":
    unittest.main()
