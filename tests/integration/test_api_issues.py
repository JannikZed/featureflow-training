"""Integration tests: API happy paths via TestClient."""

import pytest

pytestmark = pytest.mark.integration


def test_create_and_list_issues(client):
    r = client.post(
        "/api/issues",
        json={"title": "API topic", "description": "from test", "status": "open"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "API topic"
    issue_id = body["id"]

    listed = client.get("/api/issues")
    assert listed.status_code == 200
    ids = [i["id"] for i in listed.json()]
    assert issue_id in ids


def test_get_issue_not_found(client):
    r = client.get("/api/issues/99999")
    assert r.status_code == 404


def test_patch_status_and_assign(client):
    created = client.post("/api/issues", json={"title": "Patch me"}).json()
    issue_id = created["id"]

    patched = client.patch(f"/api/issues/{issue_id}", json={"status": "in_progress"})
    assert patched.status_code == 200
    assert patched.json()["status"] == "in_progress"

    assigned = client.post(
        f"/api/issues/{issue_id}/assign", json={"assignee": "alex"}
    )
    assert assigned.status_code == 200
    assert assigned.json()["assignee"] == "alex"
