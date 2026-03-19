from werkzeug.security import generate_password_hash, check_password_hash
from ..db import get_db
from ..exceptions import  LoginFailed, UserExists
from ..auth import generate_auth_token
from ..response import ok
from ..repositories.user_repository import(
    username_exists_repo,
    create_user_repo,
    get_user_by_username_repo
)
def register_service(username: str, password: str) -> dict:
    if username_exists_repo(username=username):
        raise UserExists()
    password_hash = generate_password_hash(password)
    user_id = create_user_repo(username=username, password_hash=password_hash)
    return {"user_id": user_id, "username": username}

def login_service(username: str, password: str) -> dict:

    user = get_user_by_username_repo(username=username)
    if not user:
        raise LoginFailed()
    if not check_password_hash(user["password"], password):
        raise LoginFailed()
    token = generate_auth_token({"user_id": user["id"]})
    return {"user": user, "token": token}
