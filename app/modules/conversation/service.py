from ...common.exceptions import Conflict, NotFound, BadRequest
from . import repository as conversation_repo

def _ensure_user_exists(user_id: int) -> None:
    from ..user.repository import get_user_by_id
    user = get_user_by_id(user_id=user_id)
    if not user:
        raise NotFound(code="USER_NOT_FOUND", message="user not found")
    
def get_or_create_direct_conversation(user_id: int, target_user_id: int) -> int:
    _ensure_user_exists(user_id=target_user_id)

    if user_id == target_user_id:
        raise Conflict(message="Cannot create conversation with yourself")
    conversation_dict = conversation_repo.find_direct_conversation_between_users(
        user_a_id=user_id, 
        user_b_id=target_user_id
        )
    if not conversation_dict:
        conversation_id = conversation_repo.create_conversation(type="direct")
        conversation_repo.add_conversation_member(conversation_id=conversation_id, user_id=user_id)
        conversation_repo.add_conversation_member(conversation_id=conversation_id, user_id=target_user_id)
        return conversation_id
    else:
        return conversation_dict["conversation_id"]

def list_user_conversations_paginated(
    user_id: int, 
    page: int, 
    page_size: int, 
    sort: str, 
    order: str, 
    keyword: str | None
) -> dict:
    data = conversation_repo.list_user_conversations_paginated(
        user_id=user_id, 
        page=page, 
        page_size=page_size, 
        sort=sort, 
        order=order,
        keyword=keyword
    )
    return data

def get_conversation(user_id: int, conversation_id: int) -> dict:
    if not conversation_repo.membership_exists(user_id=user_id, conversation_id=conversation_id):
        raise NotFound(code="CONVERSATION_NOT_FOUND", message="conversation not found")
    data = conversation_repo.get_conversation_by_id(conversation_id=conversation_id)
    return data
