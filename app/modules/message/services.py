from ...common.exceptions import NotFound
from . import repository as message_repo

def _ensure_conversation_member(user_id: int, conversation_id: int) -> None:
    from ..conversation.repository import membership_exists
    exists = membership_exists(user_id=user_id, conversation_id=conversation_id)
    if not exists:
        raise NotFound(code="CONVERSATION_NOT_FOUND", message="Conversation not found")

def create_message(user_id: int, conversation_id: int, content: str) -> int:
    _ensure_conversation_member(user_id=user_id, conversation_id=conversation_id)
    message_id = message_repo.create_message(
        user_id=user_id, 
        conversation_id=conversation_id, 
        content=content
    )
    return message_id

def list_messages_paginated(
    user_id: int, 
    conversation_id: int, 
    page: int,
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None
) -> dict:
    _ensure_conversation_member(user_id=user_id, conversation_id=conversation_id)
    data = message_repo.list_messages_paginated(
        conversation_id=conversation_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword
    )
    return data