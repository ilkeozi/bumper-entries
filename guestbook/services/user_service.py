from typing import List, Optional
from guestbook.models import User
from guestbook.api.dtos.user_dto import UserDTO, CreateUserDTO
from django.db.models import Count, Max
from django.core.exceptions import ObjectDoesNotExist

def get_users() -> List[UserDTO]:
    users = User.objects.annotate(
        total_messages=Count('entries'),
        last_entry_subject=Max('entries__subject'),
        last_entry_message=Max('entries__message')
    )

    return [
        UserDTO(
            id=user.id,
            name=user.name,
            total_messages=user.total_messages,
            last_entry=f"{user.last_entry_subject} | {user.last_entry_message}" if user.last_entry_subject and user.last_entry_message else ""
        )
        for user in users
    ]

def get_user_by_id(user_id: int) -> Optional[UserDTO]:
    try:
        user = User.objects.annotate(
            total_messages=Count('entries'),
            last_entry_subject=Max('entries__subject'),
            last_entry_message=Max('entries__message')
        ).get(id=user_id)
        
        return UserDTO(
            id=user.id,
            name=user.name,
            total_messages=user.total_messages,
            last_entry=f"{user.last_entry_subject} | {user.last_entry_message}" if user.last_entry_subject and user.last_entry_message else ""
        )
    except ObjectDoesNotExist:
        return None

def create_user(data: dict) -> UserDTO:
    user_data = CreateUserDTO(**data)
    user = User.objects.create(name=user_data.name)
    return UserDTO(id=user.id, name=user.name, total_messages=0, last_entry="")



def delete_user(user_id: int) -> bool:
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return True
    except ObjectDoesNotExist:
        return False
