from pydantic import BaseModel
from typing import Optional

class EntryDTO(BaseModel):
    user_name: str
    subject: str
    message: str

class UserSummaryDTO(BaseModel):
    name: str
    total_messages: int
    last_entry: Optional[str]
