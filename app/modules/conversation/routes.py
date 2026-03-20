from flask import Blueprint, request, g
from . import service as conversation_svc
from ...common.response import ok
from ...common.decorators import require_auth_token
from ...validators.common_validators import(
    get_json,
    required_int,
)
from ...utils.pagination import(
    parse_keyword,
    parse_pagination,
    parse_sorting
)

bp = Blueprint("conversation", __name__)

@bp.post("/conversations/direct")
@require_auth_token
def get_or_create_direct_conversation_route():
    data = get_json(request=request)
    target_user_id = required_int(data=data, key="target_user_id")
    user_id = g.user["user_id"]

    conversation_id = conversation_svc.get_or_create_direct_conversation(
        user_id=user_id, 
        target_user_id=target_user_id
    )
    return ok(data={"conversation_id": conversation_id}, message="Conversation created", status=200)

@bp.get("/conversations")
@require_auth_token
def list_user_conversations_paginated_route():
    page, page_size = parse_pagination(request=request)
    sort, order = parse_sorting(
        request=request, 
        allowed_fields=("id", "created_at", "updated_at"),
        default_field="updated_at"
    )
    keyword = parse_keyword(request, max_len=200)
    user_id = g.user["user_id"]

    result = conversation_svc.list_user_conversations_paginated(
        user_id=user_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword
    )
    return ok(data=result, message="Conversations", status=200)

@bp.get("/conversations/<int:conversation_id>")
@require_auth_token
def get_conversation_detail_route(conversation_id: int):
    user_id = g.user["user_id"]
    result = conversation_svc.get_conversation(user_id=user_id, conversation_id=conversation_id)
    return ok(data=result, message="Conversation", status=200)








