from flask import request, g, Blueprint
from ..decorators import require_auth_token
from ..response import ok
from ..services import message_services
from ..validators.common_validators import(
    get_json,
    required_str
)
from ..utils.pagination import(
    parse_keyword,
    parse_pagination,
    parse_sorting
)

bp = Blueprint("message", __name__)

@bp.post("/conversations/<int:conversation_id>/messages")
@require_auth_token
def create_message_route(conversation_id: int):
    data = get_json(request=request)
    content = required_str(data=data, key="content", min_len=1, max_len=4000)
    user_id = g.user["user_id"]

    message_id = message_services.create_message(
        user_id=user_id, 
        conversation_id=conversation_id, 
        content=content
    )
    return ok(data={"message_id": message_id}, message="Message created", status=201)

@bp.get("/conversations/<int:conversation_id>/messages")
@require_auth_token
def list_messages_paginated_route(conversation_id: int):
    page, page_size = parse_pagination(request=request)
    keyword = parse_keyword(request=request)
    sort, order = parse_sorting(
        request=request,
        allowed_fields=("id", "sender_id", "content", "created_at"),
        default_field="created_at"
    )

    user_id = g.user["user_id"]
    result = message_services.list_messages_paginated(
        user_id=user_id, 
        conversation_id=conversation_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword
    )
    
    return ok(data=result, message="Messages", status=200)