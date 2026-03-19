from ..exceptions import NotFound
from ..repositories.conversation_repository import membership_exists_repo
from ..repositories.message_repository import(
    list_messages_paginated_repo,
    create_massage_repo
)

def create_massage_service(user_id: int, conversation_id: int, content: str) -> int:
    if not membership_exists_repo(user_id=user_id, conversation_id=conversation_id):
        raise NotFound(code="CONVERSATION_NOT_FOUND", message="Conversation not found")
    
    massage_id = create_massage_repo(
        user_id=user_id, 
        conversation_id=conversation_id, 
        content=content
    )
    return massage_id

def list_messages_paginated_service(
    user_id: int, 
    conversation_id: int, 
    page: int,
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None
) -> dict:
    if not membership_exists_repo(user_id=user_id, conversation_id=conversation_id):
        raise NotFound(code="CONVERSATION_NOT_FOUND", message="Conversation not found")
    
    data = list_messages_paginated_repo(
        conversation_id=conversation_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword
    )
    return data