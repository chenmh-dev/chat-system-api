from ...core.db import get_db

def create_message(user_id: int, conversation_id: int, content: str) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO messages(conversation_id, sender_id, content) VALUES(?, ?, ?)",
        (conversation_id, user_id , content)
    )
    db.commit()
    return cur.lastrowid

def list_messages_paginated(
    conversation_id: int,
    page: int, 
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None
) -> dict:
    db = get_db()
    where_clause = "WHERE conversation_id = ? "

    params = [conversation_id]

    if keyword:
        where_clause += f"AND content LIKE ? "
        params.append(f"%{keyword}%")

    total_row = db.execute(f"""
        SELECT COUNT(*) AS count
        FROM messages
        {where_clause}
    """,
    tuple(params)
    ).fetchone()
    total = total_row["count"]
    total_pages = (total + page_size - 1) // page_size

    query = (f"""
        SELECT *
        FROM messages
        {where_clause}
        ORDER BY {sort} {order}
        LIMIT ? OFFSET ?
    """)
    
    offset = (page - 1) * page_size
    params.extend([page_size, offset])

    rows = db.execute(
        query,
        tuple(params)
    ).fetchall()
    
    items = [dict(r) for r in rows]
    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    }


