# tests/unit/test_entry_viewset.py
import pytest
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIRequestFactory
from guestbook.api.views.entry_views import EntryViewSet

factory = APIRequestFactory()

class TestEntryViewSet:

    @patch("guestbook.api.views.entry_views.get_entries")
    def test_list_entries(self, mock_get_entries):
        mock_get_entries.return_value = [
            {"id": 1, "user_name": "User1", "subject": "Subject1", "message": "Message1", "created_date": "2024-01-01T00:00:00Z"},
        ]
        request = factory.get("/api/entries/")
        view = EntryViewSet.as_view({"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'] == mock_get_entries.return_value

    @patch("guestbook.api.views.entry_views.create_entry")
    def test_create_entry(self, mock_create_entry):
        mock_create_entry.return_value = {
            "id": 1, "user_name": "User1", "subject": "New Subject", "message": "New Message", "created_date": "2024-01-01T00:00:00Z"
        }
        request = factory.post("/api/entries/", {"user_name": "User1", "subject": "New Subject", "message": "New Message"}, format="json")
        view = EntryViewSet.as_view({"post": "create"})
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == mock_create_entry.return_value

    @patch("guestbook.api.views.entry_views.get_entry_by_id")
    def test_retrieve_entry(self, mock_get_entry_by_id):
        mock_get_entry_by_id.return_value = {"id": 1, "user_name": "User1", "subject": "Subject1", "message": "Message1", "created_date": "2024-01-01T00:00:00Z"}
        request = factory.get("/api/entries/1/")
        view = EntryViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_get_entry_by_id.return_value

    @patch("guestbook.api.views.entry_views.update_entry")
    def test_update_entry(self, mock_update_entry):
        mock_update_entry.return_value = {"id": 1, "user_name": "User1", "subject": "Updated Subject", "message": "Updated Message", "created_date": "2024-01-01T00:00:00Z"}
        request = factory.put("/api/entries/1/", {"subject": "Updated Subject", "message": "Updated Message"}, format="json")
        view = EntryViewSet.as_view({"put": "update"})
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_update_entry.return_value

    @patch("guestbook.api.views.entry_views.delete_entry")
    def test_delete_entry(self, mock_delete_entry):
        mock_delete_entry.return_value = True
        request = factory.delete("/api/entries/1/")
        view = EntryViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch("guestbook.api.views.entry_views.get_entries")
    def test_list_entries_pagination(self, mock_get_entries):
        mock_get_entries.return_value = [
            {"id": i, "user_name": f"User{i}", "subject": f"Subject{i}", "message": f"Message{i}", "created_date": "2024-01-01T00:00:00Z"}
            for i in range(1, 11)
        ]
        request = factory.get("/api/entries/", {"page": 1, "page_size": 5})
        view = EntryViewSet.as_view({"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        expected_data = [
            {"id": i, "user_name": f"User{i}", "subject": f"Subject{i}", "message": f"Message{i}", "created_date": "2024-01-01T00:00:00Z"}
            for i in range(1, 6)
        ]
        assert response.data['results'] == expected_data

    @patch("guestbook.api.views.entry_views.get_entries")
    def test_list_entries_second_page_pagination(self, mock_get_entries):
        mock_get_entries.return_value = [
            {"id": i, "user_name": f"User{i}", "subject": f"Subject{i}", "message": f"Message{i}", "created_date": "2024-01-01T00:00:00Z"}
            for i in range(1, 11)
        ]
        request = factory.get("/api/entries/", {"page": 2, "page_size": 5})
        view = EntryViewSet.as_view({"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        expected_data = [
            {"id": i, "user_name": f"User{i}", "subject": f"Subject{i}", "message": f"Message{i}", "created_date": "2024-01-01T00:00:00Z"}
            for i in range(6, 11)
        ]
        assert response.data['results'] == expected_data
