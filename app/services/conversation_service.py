from ..exceptions import Conflict, NotFound, BadRequest
from ..repositories.user_repository import get_user_by_id
from ..repositories.conversation_repository import(
    find_direct_conversation_between_users,
    create_conversation,
    add_conversation_member,
    list_user_conversations_paginated,
    get_conversation_by_id,
    membership_exists
)

def get_or_create_direct_conversation(user_id: int, target_user_id: int) -> int:
    if user_id == target_user_id:
        raise Conflict(message="Cannot create conversation with yourself")
    data = find_direct_conversation_between_users(
        user_a_id=user_id, 
        user_b_id=target_user_id
        )
    if data is None:
        if get_user_by_id(user_id=target_user_id) is None:
            raise NotFound(code="USER_NOT_FOUND", message="user not found")
        conversation_id = create_conversation(type="direct")
        add_conversation_member(conversation_id=conversation_id, user_id=user_id)
        add_conversation_member(conversation_id=conversation_id, user_id=target_user_id)
        return conversation_id
    else:
        return data["conversation_id"]

def list_conversations_paginated(
    user_id: int, 
    page: int, 
    page_size: int, 
    sort: str, 
    order: str, 
    keyword: str | None
) -> dict:
    data = list_user_conversations_paginated(
        user_id=user_id, 
        page=page, 
        page_size=page_size, 
        sort=sort, 
        order=order,
        keyword=keyword
    )
    return data

def get_conversation(user_id: int, conversation_id: int) -> dict:
    if not membership_exists(conversation_id=conversation_id, user_id=user_id):
        raise NotFound(code="CONVERSATION_NOT_FOUND", message="conversation not found")
    data = get_conversation_by_id(conversation_id=conversation_id)
    return data
