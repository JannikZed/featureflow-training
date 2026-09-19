"""Thin HTML UI via Jinja2. Admin controls are UI-gated only."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from . import models
from .auth import get_ui_role, is_admin_ui

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(tags=["web"])


def _ctx(request: Request, **extra):
    role = get_ui_role(request)
    return {
        "request": request,
        "role": role,
        "is_admin": role == "admin",
        **extra,
    }


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    issues = models.list_issues()
    return templates.TemplateResponse(
        "index.html",
        _ctx(request, issues=issues),
    )


@router.post("/issues")
def create_issue_form(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
):
    models.create_issue(title=title.strip(), description=description.strip())
    return RedirectResponse(url="/", status_code=303)


@router.get("/issues/{issue_id}", response_class=HTMLResponse)
def issue_detail(request: Request, issue_id: int):
    issue = models.get_issue(issue_id)
    if not issue:
        return templates.TemplateResponse(
            "index.html",
            _ctx(request, issues=models.list_issues(), error="Issue not found"),
            status_code=404,
        )
    comments = models.list_comments(issue_id)
    return templates.TemplateResponse(
        "issue_detail.html",
        _ctx(request, issue=issue, comments=comments),
    )


@router.post("/issues/{issue_id}/comments")
def add_comment_form(
    issue_id: int,
    body: str = Form(...),
    author: str = Form("anonymous"),
):
    if models.get_issue(issue_id) is None:
        return RedirectResponse(url="/", status_code=303)
    models.add_comment(issue_id, body=body.strip(), author=author.strip() or "anonymous")
    return RedirectResponse(url=f"/issues/{issue_id}", status_code=303)


@router.post("/issues/{issue_id}/status")
def change_status_form(
    request: Request,
    issue_id: int,
    status: str = Form(...),
):
    """UI-gated: only shown to admins. API equivalent is ungated."""
    if not is_admin_ui(request):
        return RedirectResponse(url=f"/issues/{issue_id}?denied=1", status_code=303)
    if models.get_issue(issue_id):
        try:
            models.update_issue(issue_id, status=status)
        except ValueError:
            pass
    return RedirectResponse(url=f"/issues/{issue_id}", status_code=303)


@router.post("/issues/{issue_id}/assign")
def assign_form(
    request: Request,
    issue_id: int,
    assignee: str = Form(""),
):
    """UI-gated: only shown to admins. API equivalent is ungated."""
    if not is_admin_ui(request):
        return RedirectResponse(url=f"/issues/{issue_id}?denied=1", status_code=303)
    if models.get_issue(issue_id):
        models.update_issue(issue_id, assignee=assignee.strip() or None)
    return RedirectResponse(url=f"/issues/{issue_id}", status_code=303)


@router.post("/issues/{issue_id}/delete")
def delete_form(request: Request, issue_id: int):
    """UI-gated: only shown to admins. API equivalent is ungated."""
    if not is_admin_ui(request):
        return RedirectResponse(url="/?denied=1", status_code=303)
    models.delete_issue(issue_id)
    return RedirectResponse(url="/", status_code=303)


@router.post("/set-role")
def set_role(role: str = Form("user")):
    """Toy role switcher — sets ff_role cookie for UI gating demos."""
    value = "admin" if role.strip().lower() == "admin" else "user"
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="ff_role", value=value, httponly=False, samesite="lax")
    return response
