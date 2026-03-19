from ..db import get_db
from .conversation_repository import membership_exists

def list_messages_paginated(
    user_id: int, 
    conversation_id: int,
    page: int, 
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None
):
    if not membership_exists(conversation_id=conversation_id, user_id=user_id):
        raise 
    db = get_db()
    where_clause = "WHERE sender_id = ? "

    params = [user_id]

    if keyword:
        where_clause += f"AND content LIKE ? "
        params.append(f"%{keyword}%")

    db.execute(f"""
        SELECT COUNT(*)
        FROM messages
        {where_clause}
    """,
    tuple(params)
    )





