# tests/e2e/test_endpoints.py
import pytest
import requests
from django.urls import reverse
from django.test import LiveServerTestCase

# Base URL (use live server for test isolation)
BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.django_db
class TestUserEndpoints(LiveServerTestCase):
    def setUp(self):
        # Initialize the live server URL to use within tests
        self.client = requests.Session()
        self.base_url = self.live_server_url

    def test_create_user(self):
        url = f"{self.base_url}/api/users/"
        payload = {"name": "TestUserE2E"}
        response = self.client.post(url, json=payload)
        
        assert response.status_code == 201
        assert response.json()["name"] == "TestUserE2E"

    def test_get_user_list(self):
        # First, create a user
        self.client.post(f"{self.base_url}/api/users/", json={"name": "User1"})

        # Then, get the user list
        url = f"{self.base_url}/api/users/"
        response = self.client.get(url)

        assert response.status_code == 200
        assert "User1" in [user["name"] for user in response.json()]


    def test_delete_user(self):
        # Create a user
        create_response = self.client.post(f"{self.base_url}/api/users/", json={"name": "ToDelete"})
        user_id = create_response.json()["id"]

        # Delete the user
        url = f"{self.base_url}/api/users/{user_id}/"
        response = self.client.delete(url)

        assert response.status_code == 204

        # Verify deletion
        get_response = self.client.get(f"{self.base_url}/api/users/")
        assert "ToDelete" not in [user["name"] for user in get_response.json()]
