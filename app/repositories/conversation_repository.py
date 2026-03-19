from ..db import get_db

def create_conversation(type: str) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO conversations(type) VALUES (?)",
        (type,)
    )
    db.commit()
    return cur.lastrowid

def add_conversation_member(conversation_id: int, user_id: int) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO conversation_members(conversation_id, user_id) VALUES(?, ?)",
        (conversation_id, user_id)
    )
    db.commit()
    return cur.lastrowid

def find_direct_conversation_between_users(
    user_a_id: int, 
    user_b_id: int
) -> dict | None:
    db = get_db()
    row = db.execute("""
        SELECT c.id AS conversation_id
        FROM conversations AS c
        JOIN conversation_members AS cm_a ON c.id = cm_a.conversation_id
        JOIN conversation_members AS cm_b ON c.id = cm_b.conversation_id
        WHERE c.type = "direct"
        AND cm_a.user_id = ?
        AND cm_b.user_id = ?    
    """,
    (user_a_id, user_b_id)
    ).fetchone()
    
    return dict(row) if row else None
    

def get_conversation_by_id(conversation_id: int) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM conversations WHERE id = ?",
        (conversation_id,)
    ).fetchone()
    return dict(row) if row else None

def list_user_conversations_paginated(
    user_id: int, 
    page: int, 
    page_size: int, 
    sort: str, 
    order: str,
    keyword: str | None
) -> dict:  
    db = get_db()
    where_clause = "WHERE cm.user_id = ? "
    params = [user_id]
    if keyword:
        where_clause += f"AND c.type LIKE ? "
        params.append(f"%{keyword}%")
    
    total_row = db.execute(f"""
        SELECT COUNT(*) AS count 
        FROM conversations AS c
        JOIN conversation_members AS cm ON c.id = cm.conversation_id            
        {where_clause}""",
        tuple(params)
    ).fetchone()
    total = total_row["count"]
    total_pages = (total + page_size - 1) // page_size

    query = (f"""
        SELECT c.*
        FROM conversations AS c
        JOIN conversation_members AS cm ON c.id = cm.conversation_id
        {where_clause}
        ORDER BY {sort} {order}
        LIMIT ? offset ?
    """)
    offset = (page - 1) * page_size
    params += [page_size, offset]

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

def membership_exists(conversation_id: int, user_id: int) -> bool:
    db = get_db()
    row = db.execute(
        "SELECT id FROM conversation_members WHERE conversation_id = ? AND user_id = ?",
        (conversation_id, user_id)
    ).fetchone()

    return True if row else False

def list_conversation_members(conversation_id: int) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT user_id FROM conversation_members WHERE conversation_id = ?",
        (conversation_id,)
    ).fetchall()

    return [dict(r) for r in rows]

def update_conversation_updated_at(conversation_id: int) -> bool:
    db = get_db()
    cur = db.execute(
        "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (conversation_id,)
    )
    if cur.rowcount == 0:
        return False
    db.commit()
    return True
