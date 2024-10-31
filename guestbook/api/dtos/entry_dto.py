from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class EntryDTO(BaseModel):
    id: int
    user_name: str
    subject: str
    message: str
    created_date: datetime

class CreateEntryDTO(BaseModel):
    user_name: str = Field(..., max_length=100, min_length=2)
    subject: str = Field(..., max_length=200, min_length=1)
    message: str = Field(..., min_length=1)

    @field_validator('user_name')
    def validate_user_name(cls, value):
        if not value.isalnum():
            raise ValueError("User name should contain only alphanumeric characters")
        return value

    @field_validator('subject')
    def validate_subject(cls, value):
        prohibited_words = ["spam", "ad"]
        if any(word in value.lower() for word in prohibited_words):
            raise ValueError("Subject contains prohibited words")
        return value

class UpdateEntryDTO(BaseModel):
    subject: str = Field(..., max_length=200, min_length=1)
    message: str = Field(..., min_length=1)

    @field_validator('subject')
    def validate_subject(cls, value):
        prohibited_words = ["spam", "ad"]
        if any(word in value.lower() for word in prohibited_words):
            raise ValueError("Subject contains prohibited words")
        return value
