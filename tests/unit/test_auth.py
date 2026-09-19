"""Unit tests for toy role helper (UI-facing)."""

from unittest.mock import MagicMock

import pytest

from app.auth import get_ui_role, is_admin_ui

pytestmark = pytest.mark.unit


def _request(header: str = "", cookie: str = ""):
    req = MagicMock()
    req.headers.get.side_effect = lambda k, default="": header if k == "X-User-Role" else default
    req.cookies.get.side_effect = lambda k, default="": cookie if k == "ff_role" else default
    return req


def test_header_admin_wins():
    assert get_ui_role(_request(header="admin")) == "admin"
    assert is_admin_ui(_request(header="admin")) is True


def test_cookie_user():
    assert get_ui_role(_request(cookie="user")) == "user"
    assert is_admin_ui(_request(cookie="user")) is False
