"""E2E HTTP-flow: create → list → comment (and read back)."""

import pytest

pytestmark = pytest.mark.e2e


def test_create_list_comment_flow(client):
    # Create
    create = client.post(
        "/api/issues",
        json={
            "title": "E2E flow issue",
            "description": "full path",
            "status": "open",
        },
    )
    assert create.status_code == 201
    issue = create.json()
    issue_id = issue["id"]

    # List
    listed = client.get("/api/issues")
    assert listed.status_code == 200
    assert any(i["id"] == issue_id for i in listed.json())

    # Comment
    comment = client.post(
        f"/api/issues/{issue_id}/comments",
        json={"author": "trainer", "body": "Looks good on the flow"},
    )
    assert comment.status_code == 201
    assert comment.json()["body"] == "Looks good on the flow"

    # Read comments
    comments = client.get(f"/api/issues/{issue_id}/comments")
    assert comments.status_code == 200
    assert len(comments.json()) == 1
    assert comments.json()[0]["author"] == "trainer"

    # Detail
    detail = client.get(f"/api/issues/{issue_id}")
    assert detail.status_code == 200
    assert detail.json()["title"] == "E2E flow issue"
