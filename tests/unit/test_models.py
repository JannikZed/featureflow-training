"""Unit tests for issue model helpers."""

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit


@pytest.fixture()
def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_file = tmp_path / "unit.db"
    monkeypatch.setattr("app.database.DB_PATH", db_file)
    from app.database import init_db
    from app import models

    init_db()
    return models


def test_create_and_get_issue(db):
    created = db.create_issue(title="Unit topic", description="d", status="open")
    assert created["id"] >= 1
    assert created["title"] == "Unit topic"
    assert created["status"] == "open"
    fetched = db.get_issue(created["id"])
    assert fetched is not None
    assert fetched["title"] == "Unit topic"


def test_invalid_status_raises(db):
    with pytest.raises(ValueError, match="Invalid status"):
        db.create_issue(title="Bad", status="nope")


def test_get_ui_role_defaults_to_user():
    from unittest.mock import MagicMock
    from app.auth import get_ui_role

    req = MagicMock()
    req.headers.get.return_value = ""
    req.cookies.get.return_value = ""
    assert get_ui_role(req) == "user"
