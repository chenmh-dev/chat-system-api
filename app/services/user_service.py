from ..repositories import user_repository
from ..exceptions import NotFound
def get_user(user_id: int) -> dict:

    user = user_repository.get_user_by_id(user_id=user_id)
    if not user:
        raise NotFound(code="USER_NOT_FOUND", message="User not found")
    return user