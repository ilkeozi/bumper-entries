import pytest
import requests
from django.test import LiveServerTestCase

@pytest.mark.django_db
class TestEntryEndpoints(LiveServerTestCase):
    def setUp(self):
        self.client = requests.Session()
        self.base_url = self.live_server_url

    def test_create_entry(self):
        # Assume a user exists for this entry
        user_response = self.client.post(f"{self.base_url}/api/users/", json={"name": "EntryUser"})
        user_id = user_response.json()["id"]

        url = f"{self.base_url}/api/entries/"
        payload = {"user_name": "EntryUser", "subject": "Test Subject", "message": "Test Message"}
        response = self.client.post(url, json=payload)
        assert response.status_code == 201
        assert response.json()["subject"] == "Test Subject"

    def test_get_entries_list(self):
        # Create an entry to ensure there’s data to fetch
        self.client.post(f"{self.base_url}/api/users/", json={"name": "EntryUser"})
        self.client.post(f"{self.base_url}/api/entries/", json={"user_name": "EntryUser", "subject": "Subject1", "message": "Message1"})

        url = f"{self.base_url}/api/entries/"
        response = self.client.get(url)
        assert response.status_code == 200
        assert "Subject1" in [entry["subject"] for entry in response.json()]

    def test_delete_entry(self):
        # Create an entry
        self.client.post(f"{self.base_url}/api/users/", json={"name": "EntryUser"})
        create_response = self.client.post(f"{self.base_url}/api/entries/", json={"user_name": "EntryUser", "subject": "ToDelete", "message": "Message"})

        entry_id = create_response.json()["id"]
        url = f"{self.base_url}/api/entries/{entry_id}/"
        response = self.client.delete(url)
        assert response.status_code == 204
