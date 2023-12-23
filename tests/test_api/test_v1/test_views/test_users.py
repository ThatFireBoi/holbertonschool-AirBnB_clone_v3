#!/usr/bin/python3
"""Unittest for user.py"""

import unittest
import json
from models import storage
from models.user import User
from api.v1.app import app
from api.v1.views.users import *


class TestUsers(unittest.TestCase):
    """Test cases for the users route"""

    def setUp(self):
        """Sets up the client for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_users(self):
        """Tests for a 200 status code"""
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        """Tests for a specific user"""
        user = User(email="test@test.com", password="test")
        user.save()
        response = self.app.get(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """Tests user deletion"""
        user = User(email="test2@test.com", password="test")
        user.save()
        response = self.app.delete(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """Tests user creation"""
        response = self.app.post('/api/v1/users', data=json.dumps(
            {"email": "test3@test.com", "password": "test"}),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_update_user(self):
        """Tests user update"""
        user = User(email="test4@test.com", password="test")
        user.save()
        response = self.app.put(f'/api/v1/users/{user.id}',
                                data=json.dumps({"email": "newtest@test.com"}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
