"""
Toy role helper for the HTML UI only.

Reads X-User-Role header or ff_role cookie.
Values: admin | user (default user).

IMPORTANT: This is intentionally NOT used by the REST API.
The security lab demonstrates that UI gating != AuthZ.
"""

from typing import Literal

from fastapi import Request

Role = Literal["admin", "user"]


def get_ui_role(request: Request) -> Role:
    header = request.headers.get("X-User-Role", "").strip().lower()
    if header in ("admin", "user"):
        return header  # type: ignore[return-value]
    cookie = request.cookies.get("ff_role", "").strip().lower()
    if cookie in ("admin", "user"):
        return cookie  # type: ignore[return-value]
    return "user"


def is_admin_ui(request: Request) -> bool:
    return get_ui_role(request) == "admin"
