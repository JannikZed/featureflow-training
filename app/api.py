"""
REST API under /api/...

Intentionally does NOT enforce authorization on privileged updates
(status changes, assignment, delete). That gap is the teaching point.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException

from . import models
from .schemas import (
    AssignRequest,
    CommentCreate,
    CommentOut,
    IssueCreate,
    IssueOut,
    IssueUpdate,
)

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/issues", response_model=list[IssueOut])
def list_issues():
    return models.list_issues()


@router.post("/issues", response_model=IssueOut, status_code=201)
def create_issue(payload: IssueCreate):
    try:
        return models.create_issue(
            title=payload.title,
            description=payload.description,
            status=payload.status,
            assignee=payload.assignee,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/issues/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: int):
    issue = models.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.patch("/issues/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: int, payload: IssueUpdate):
    """Update any fields including status/assignee — no AuthZ check."""
    if models.get_issue(issue_id) is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    data = payload.model_dump(exclude_unset=True)
    try:
        return models.update_issue(issue_id, **data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/issues/{issue_id}/assign", response_model=IssueOut)
def assign_issue(issue_id: int, payload: AssignRequest):
    """Assign (or unassign) an issue — no AuthZ check."""
    if models.get_issue(issue_id) is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return models.update_issue(issue_id, assignee=payload.assignee)


@router.delete("/issues/{issue_id}", status_code=204)
def delete_issue(issue_id: int):
    """Delete an issue — no AuthZ check."""
    if not models.delete_issue(issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    return None


@router.get("/issues/{issue_id}/comments", response_model=list[CommentOut])
def list_comments(issue_id: int):
    if models.get_issue(issue_id) is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return models.list_comments(issue_id)


@router.post(
    "/issues/{issue_id}/comments",
    response_model=CommentOut,
    status_code=201,
)
def add_comment(issue_id: int, payload: CommentCreate):
    comment = models.add_comment(
        issue_id, body=payload.body, author=payload.author
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return comment
