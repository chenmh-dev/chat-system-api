from typing import Any
from ..exceptions import BadRequest


def get_json(request) -> dict:
    data = request.get_json(silent=True)

    if data is None:
        raise BadRequest(message="Invalid json body")

    if not isinstance(data, dict):
        raise BadRequest(message="Json body must be an object")
    return data


def required_str(
    data: dict,
    key: str,
    *,
    min_len: int = 1,
    max_len: int = 2000,
) -> str:
    val = data.get(key)

    if val is None:
        raise BadRequest(message=f"{key} is required")

    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")

    s = val.strip()

    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")

    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")
    return s


def optional_str(
    data: dict,
    key: str,
    *,
    min_len: int = 1,
    max_len: int = 2000,
) -> str | None:
    val = data.get(key)

    if val is None:
        return None

    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")

    s = val.strip()

    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")

    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")
    return s


def require_any(*values: Any, message: str = "No fields to update") -> None:
    if all(v is None for v in values):
        raise BadRequest(message=message)


def validate_task_status(
    data: dict, 
    required: bool = True,
    default_status: str | None = None,
    default_status_fields: tuple[str, ...] = ("todo", "in_progress", "done")
) -> str | None:
    val = data.get("status", None)

    if not isinstance(val, str):
        raise BadRequest(message="Status must be a string")
    
    if val is None:
        if required:
            raise BadRequest(message="Status is required")
        else:
            return default_status
    
    status = val.strip().lower()
    if status not in default_status_fields:
        raise BadRequest(message=f"Status must be one of {list(default_status_fields)}")
    return status


def required_int(
    data: dict,
    key: str,
    *,
    min_size: int = 1,
    max_size: int = 9999999,
) -> int | None:
    val = data.get(key)

    if val is None:
        raise BadRequest(message=f"{key} is required")
    
    if not isinstance(val, int):
        raise BadRequest(message=f"{key} must be a integer")

    if val < min_size:
        raise BadRequest(message=f"{key} is too small")
    
    if val > max_size:
        raise BadRequest(message=f"{key} is too big")
    return val