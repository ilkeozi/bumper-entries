from typing import List, Optional
from guestbook.models import Entry, User
from guestbook.api.dtos.entry_dto import EntryDTO, CreateEntryDTO, UpdateEntryDTO
from django.core.exceptions import ObjectDoesNotExist

def get_entries() -> List[EntryDTO]:
    entries = Entry.objects.all()
    return [
        EntryDTO(
            id=entry.id,
            user_name=entry.user.name,
            subject=entry.subject,
            message=entry.message,
            created_date=entry.created_date
        )
        for entry in entries
    ]

def get_entry_by_id(entry_id: int) -> Optional[EntryDTO]:
    try:
        entry = Entry.objects.get(id=entry_id)
        return EntryDTO(
            id=entry.id,
            user_name=entry.user.name,
            subject=entry.subject,
            message=entry.message,
            created_date=entry.created_date
        )
    except ObjectDoesNotExist:
        return None

def create_entry(data: dict) -> EntryDTO:
    entry_data = CreateEntryDTO(**data)
    user, _ = User.objects.get_or_create(name=entry_data.user_name)
    entry = Entry.objects.create(
        user=user,
        subject=entry_data.subject,
        message=entry_data.message
    )
    return EntryDTO(
        id=entry.id,
        user_name=user.name,
        subject=entry.subject,
        message=entry.message,
        created_date=entry.created_date
    )

def update_entry(entry_id: int, data: dict) -> Optional[EntryDTO]:
    try:
        entry = Entry.objects.get(id=entry_id)
        update_data = UpdateEntryDTO(**data)
        entry.subject = update_data.subject
        entry.message = update_data.message
        entry.save()
        return EntryDTO(
            id=entry.id,
            user_name=entry.user.name,
            subject=entry.subject,
            message=entry.message,
            created_date=entry.created_date
        )
    except ObjectDoesNotExist:
        return None

def delete_entry(entry_id: int) -> bool:
    try:
        entry = Entry.objects.get(id=entry_id)
        entry.delete()
        return True
    except ObjectDoesNotExist:
        return False
