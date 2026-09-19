"""Shared fixtures: isolated SQLite DB per test session/function."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """App TestClient backed by a fresh temporary database."""
    db_file = tmp_path / "test_featureflow.db"
    monkeypatch.setattr("app.database.DB_PATH", db_file)

    from app.database import init_db
    from app.main import app

    init_db()
    with TestClient(app) as c:
        yield c
