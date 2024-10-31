from pydantic import BaseModel, Field, field_validator
from typing import Optional

class UserDTO(BaseModel):
    id: int
    name: str
    total_messages: int
    last_entry: Optional[str] = None

class CreateUserDTO(BaseModel):
    name: str = Field(..., max_length=100, min_length=2)

    @field_validator('name')
    def validate_name(cls, value):
        if not value.isalnum():
            raise ValueError("Name should contain only alphanumeric characters")
        return value


