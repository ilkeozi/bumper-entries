import pytest
from guestbook.api.serializers import (
    EntryDTOSerializer, CreateEntryDTOSerializer, 
    UpdateEntryDTOSerializer, UserDTOSerializer, CreateUserDTOSerializer
)
from datetime import datetime
from rest_framework.exceptions import ValidationError

def test_entry_dto_serializer():
    dto_data = {
        "id": 1,
        "user_name": "TestUser",
        "subject": "Test Subject",
        "message": "Test Message",
        "created_date": datetime.now()
    }
    serializer = EntryDTOSerializer(data=dto_data)
    assert serializer.is_valid()
    assert serializer.validated_data["user_name"] == "TestUser"

def test_create_entry_dto_serializer_valid_data():
    valid_data = {
        "user_name": "ValidUser",
        "subject": "Valid Subject",
        "message": "This is a valid message."
    }
    serializer = CreateEntryDTOSerializer(data=valid_data)
    assert serializer.is_valid()

def test_create_entry_dto_serializer_invalid_user_name():
    invalid_data = {
        "user_name": "Invalid@User",
        "subject": "Subject",
        "message": "Message"
    }
    serializer = CreateEntryDTOSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "user_name" in serializer.errors

def test_update_entry_dto_serializer_valid_data():
    valid_data = {"subject": "Updated Subject", "message": "Updated message"}
    serializer = UpdateEntryDTOSerializer(data=valid_data)
    assert serializer.is_valid()

def test_user_dto_serializer():
    user_data = {
        "id": 1,
        "name": "TestUser",
        "total_messages": 5,
        "last_entry": "Last message | Hello"
    }
    serializer = UserDTOSerializer(data=user_data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "TestUser"

def test_create_user_dto_serializer_valid_data():
    valid_data = {"name": "ValidUser"}
    serializer = CreateUserDTOSerializer(data=valid_data)
    assert serializer.is_valid()

def test_create_user_dto_serializer_invalid_name():
    invalid_data = {"name": "Invalid@User"}
    serializer = CreateUserDTOSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
