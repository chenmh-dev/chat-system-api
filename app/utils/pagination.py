from ..exceptions import BadRequest

def parse_pagination(
    request,
    *,
    default_page: int = 1,
    default_page_size: int = 10,
    max_page_size: int = 50,
) -> tuple[int, int]:
    page_raw = request.args.get("page", str(default_page))
    page_size_raw = request.args.get("page_size", str(default_page_size))

    try:
        page = int(page_raw)
        page_size = int(page_size_raw)
    except ValueError:
        raise BadRequest(message="page and page_size must be integers")

    if page < 1:
        raise BadRequest(message="page must be >= 1")

    if page_size < 1 or page_size > max_page_size:
        raise BadRequest(message=f"page_size must be between 1 and {max_page_size}")

    return page, page_size


def parse_sorting(
    request,
    *,
    allowed_fields: tuple[str, ...],
    default_field: str = "id",
    default_order: str = "desc",
) -> tuple[str, str]:
    sort = request.args.get("sort", default_field)
    order = request.args.get("order", default_order).lower()

    if sort not in allowed_fields:
        raise BadRequest(message=f"sort must be one of {list(allowed_fields)}")

    if order not in ("asc", "desc"):
        raise BadRequest(message="order must be 'asc' or 'desc'")

    return sort, order


def parse_keyword(request, max_len: int = 100) -> str | None:
    keyword = request.args.get("keyword")

    if keyword is None:
        return None

    keyword = str(keyword).strip()

    if len(keyword) > max_len:
        raise BadRequest(message="keyword is too long")

    return keyword if keyword else None