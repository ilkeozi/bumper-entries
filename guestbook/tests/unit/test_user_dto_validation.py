import pytest
from pydantic import ValidationError
from guestbook.api.dtos.user_dto import CreateUserDTO, UserDTO

def test_create_user_dto_valid_data():
    dto = CreateUserDTO(name="ValidUser")
    assert dto.name == "ValidUser"

def test_create_user_dto_invalid_name_non_alphanumeric():
    with pytest.raises(ValidationError) as exc_info:
        CreateUserDTO(name="Invalid@User")
    assert "Name should contain only alphanumeric characters" in str(exc_info.value)

def test_create_user_dto_invalid_name_too_short():
    with pytest.raises(ValidationError) as exc_info:
        CreateUserDTO(name="A") 
    assert "String should have at least 2 characters" in str(exc_info.value)

def test_create_user_dto_invalid_name_too_long():
    with pytest.raises(ValidationError) as exc_info:
        CreateUserDTO(name="A" * 101)  
    assert "String should have at most 100 characters" in str(exc_info.value)

def test_user_dto_optional_last_entry():
    dto = UserDTO(id=1, name="UserTest", total_messages=5)
    assert dto.last_entry is None

def test_user_dto_with_last_entry():
    dto = UserDTO(id=1, name="UserTest", total_messages=5, last_entry="Last message | Hello")
    assert dto.last_entry == "Last message | Hello"
