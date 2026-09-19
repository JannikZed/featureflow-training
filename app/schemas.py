"""Pydantic request/response models."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


Status = Literal["open", "in_progress", "done"]


class IssueCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: Status = "open"
    assignee: Optional[str] = None


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[Status] = None
    assignee: Optional[str] = None


class AssignRequest(BaseModel):
    assignee: Optional[str] = None


class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)
    author: str = "anonymous"


class IssueOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    assignee: Optional[str]
    created_at: str


class CommentOut(BaseModel):
    id: int
    issue_id: int
    author: str
    body: str
    created_at: str
