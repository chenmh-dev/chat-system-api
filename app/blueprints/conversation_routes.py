from flask import Blueprint, request, g
from ..response import ok
from ..decorators import require_auth_token
from ..services.conversation_service import(
    get_or_create_direct_conversation
)
from ..validators.common_validators import(
    get_json,
    required_int,
)
bp = Blueprint("conversation", __name__)

@bp.post("/conversations/direct")
@require_auth_token
def get_or_create_direct_conversation_route():
    data = get_json(request)
    target_user_id = required_int(data, "target_user_id")
    user_id = g.user["user_id"]

    conversation_id = get_or_create_direct_conversation(
        user_id=user_id, 
        target_user_id=target_user_id
    )
    return ok(data={"conversation_id": conversation_id}, message="Coversation created", status=200)

# @bp.get("/conversations")
# @require_auth_token
# def 










