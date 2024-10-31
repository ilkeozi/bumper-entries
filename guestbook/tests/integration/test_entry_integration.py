import pytest
from rest_framework import status
from rest_framework.test import APIClient
from guestbook.models import User, Entry

client = APIClient()

@pytest.mark.django_db
def test_entry_lifecycle():
    user_data = {"name": "IntegrationUser"}
    entry_data = {
        "user_name": "IntegrationUser",
        "subject": "Test Subject",
        "message": "Test Message"
    }
    client.post("/api/users/", data=user_data, format="json")
    create_response = client.post("/api/entries/", data=entry_data, format="json")
    assert create_response.status_code == status.HTTP_201_CREATED

    entry_id = create_response.data['id']

    retrieve_response = client.get(f"/api/entries/{entry_id}/")
    assert retrieve_response.status_code == status.HTTP_200_OK
    assert retrieve_response.data['subject'] == "Test Subject"

    update_data = {"subject": "Updated Subject", "message": "Updated Message"}
    update_response = client.put(f"/api/entries/{entry_id}/", data=update_data, format="json")
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data['subject'] == "Updated Subject"

    delete_response = client.delete(f"/api/entries/{entry_id}/")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    confirm_delete_response = client.get(f"/api/entries/{entry_id}/")
    assert confirm_delete_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_entry_pagination():
    user_data = {"name": "PaginationUser"}
    client.post("/api/users/", data=user_data, format="json")
    for i in range(10):
        entry_data = {
            "user_name": "PaginationUser",
            "subject": f"Test Subject {i+1}",
            "message": f"Test Message {i+1}"
        }
        client.post("/api/entries/", data=entry_data, format="json")

    paginated_response_1 = client.get("/api/entries/", {"page": 1, "page_size": 5})
    assert paginated_response_1.status_code == status.HTTP_200_OK
    assert len(paginated_response_1.data['results']) == 5
    assert 'next' in paginated_response_1.data
    assert 'previous' in paginated_response_1.data
    assert paginated_response_1.data['next'] is not None

    paginated_response_2 = client.get("/api/entries/", {"page": 2, "page_size": 5})
    assert paginated_response_2.status_code == status.HTTP_200_OK
    assert len(paginated_response_2.data['results']) == 5
