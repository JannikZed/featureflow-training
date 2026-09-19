"""Data-access helpers for issues and comments."""

from typing import Any, Optional

from .database import db_session


VALID_STATUSES = ("open", "in_progress", "done")


def _row_to_dict(row) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return dict(row)


def list_issues() -> list[dict[str, Any]]:
    with db_session() as conn:
        rows = conn.execute(
            "SELECT * FROM issues ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_issue(issue_id: int) -> Optional[dict[str, Any]]:
    with db_session() as conn:
        row = conn.execute(
            "SELECT * FROM issues WHERE id = ?", (issue_id,)
        ).fetchone()
        return _row_to_dict(row)


def create_issue(
    title: str,
    description: str = "",
    status: str = "open",
    assignee: Optional[str] = None,
) -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    with db_session() as conn:
        cur = conn.execute(
            """
            INSERT INTO issues (title, description, status, assignee)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, status, assignee or None),
        )
        issue_id = cur.lastrowid
    return get_issue(issue_id)  # type: ignore[return-value]


def update_issue(issue_id: int, **fields) -> Optional[dict[str, Any]]:
    """Update issue fields. Intentionally no authorization check."""
    allowed = {"title", "description", "status", "assignee"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if "status" in updates and updates["status"] not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {updates['status']}")
    if not updates:
        return get_issue(issue_id)
    if "assignee" in updates and updates["assignee"] == "":
        updates["assignee"] = None

    cols = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [issue_id]
    with db_session() as conn:
        conn.execute(f"UPDATE issues SET {cols} WHERE id = ?", values)
    return get_issue(issue_id)


def delete_issue(issue_id: int) -> bool:
    """Delete an issue. Intentionally no authorization check."""
    with db_session() as conn:
        cur = conn.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        return cur.rowcount > 0


def list_comments(issue_id: int) -> list[dict[str, Any]]:
    with db_session() as conn:
        rows = conn.execute(
            """
            SELECT * FROM comments
            WHERE issue_id = ?
            ORDER BY id ASC
            """,
            (issue_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def add_comment(
    issue_id: int, body: str, author: str = "anonymous"
) -> Optional[dict[str, Any]]:
    if get_issue(issue_id) is None:
        return None
    with db_session() as conn:
        cur = conn.execute(
            """
            INSERT INTO comments (issue_id, author, body)
            VALUES (?, ?, ?)
            """,
            (issue_id, author or "anonymous", body),
        )
        comment_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM comments WHERE id = ?", (comment_id,)
        ).fetchone()
        return dict(row)
