# Security lab notes (trainer)

Short factual brief for the day-2 AuthZ exercise.

## What is gated

- The **HTML UI** reads role from `ff_role` cookie or `X-User-Role` header (`admin` \| `user`).
- Admin-only controls (status change, assign, delete) are **hidden** for non-admins and the matching form POST handlers in `app/web.py` refuse non-admin roles with a redirect.

## What is not gated

- REST endpoints under `/api/...` perform **no** authorization checks.
- In particular these succeed for any caller:
  - `PATCH /api/issues/{id}` (status, assignee, title, …)
  - `POST /api/issues/{id}/assign`
  - `DELETE /api/issues/{id}`

## Teaching point

UI gating ≠ AuthZ. A user who never sees the admin buttons can still change status/assignee or delete issues via the API (classic missing AuthZ / IDOR-style demo). There is no real JWT/OAuth; do not treat the cookie as a security boundary.

## Suggested demo

1. Browse as `user` — confirm admin panel is absent.
2. `curl` a status change or delete on `/api/issues/{id}` without any admin header — observe success.
3. Ask participants to add server-side AuthZ on the privileged API routes (and optionally share the same helper as the UI).
