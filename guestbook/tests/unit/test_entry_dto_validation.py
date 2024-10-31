import pytest
from pydantic import ValidationError
from guestbook.api.dtos.entry_dto import CreateEntryDTO, UpdateEntryDTO

def test_create_entry_dto_valid_data():
    dto = CreateEntryDTO(user_name="ValidUser", subject="Valid Subject", message="This is a valid message.")
    assert dto.user_name == "ValidUser"
    assert dto.subject == "Valid Subject"
    assert dto.message == "This is a valid message."

def test_create_entry_dto_invalid_user_name():
    with pytest.raises(ValidationError) as exc_info:
        CreateEntryDTO(user_name="Invalid@Name", subject="Subject", message="Message")
    assert "User name should contain only alphanumeric characters" in str(exc_info.value)

def test_create_entry_dto_invalid_subject_prohibited_word():
    with pytest.raises(ValidationError) as exc_info:
        CreateEntryDTO(user_name="ValidUser", subject="This is spam", message="Message")
    assert "Subject contains prohibited words" in str(exc_info.value)

def test_create_entry_dto_invalid_subject_length():
    with pytest.raises(ValidationError):
        CreateEntryDTO(user_name="ValidUser", subject="a" * 201, message="Message")  # Exceeds max length

def test_create_entry_dto_invalid_message_length():
    with pytest.raises(ValidationError):
        CreateEntryDTO(user_name="ValidUser", subject="Subject", message="")  # Empty message not allowed

def test_update_entry_dto_valid_data():
    dto = UpdateEntryDTO(subject="Updated Subject", message="Updated message")
    assert dto.subject == "Updated Subject"
    assert dto.message == "Updated message"

def test_update_entry_dto_invalid_subject_prohibited_word():
    with pytest.raises(ValidationError) as exc_info:
        UpdateEntryDTO(subject="This is an ad", message="Message")
    assert "Subject contains prohibited words" in str(exc_info.value)

def test_update_entry_dto_invalid_subject_length():
    with pytest.raises(ValidationError):
        UpdateEntryDTO(subject="a" * 201, message="Message")  # Exceeds max length

def test_update_entry_dto_invalid_message_length():
    with pytest.raises(ValidationError):
        UpdateEntryDTO(subject="Valid Subject", message="")  # Empty message not allowed
