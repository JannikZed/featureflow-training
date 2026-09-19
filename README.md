# FeatureFlow Training

Brownfield starter for the 2026 Copilot / Agents training.

**This is a training starter — intentionally imperfect.** It ships with a thin HTML UI, a SQLite-backed REST API, almost no tests, and a deliberate authorization gap for day-2 security labs. Do not use it in production.

## Clone

```bash
git clone https://github.com/JannikZed/featureflow-training
cd featureflow-training
```

## Run locally

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/ for the UI. API docs: http://127.0.0.1:8000/docs

## Domain

Issues / features with:

| Field | Notes |
|-------|--------|
| `id` | integer PK |
| `title` | required |
| `description` | free text |
| `status` | `open` \| `in_progress` \| `done` |
| `assignee` | optional |
| `created_at` | set on create |

Comments hang off issues. Assignment and status changes are first-class API operations.

## Example curls

```bash
# Create an issue
curl -s -X POST http://127.0.0.1:8000/api/issues \
  -H 'Content-Type: application/json' \
  -d '{"title":"Dark mode","description":"Theme toggle","status":"open"}'

# List issues
curl -s http://127.0.0.1:8000/api/issues

# Update status (no AuthZ on API — by design for the lab)
curl -s -X PATCH http://127.0.0.1:8000/api/issues/1 \
  -H 'Content-Type: application/json' \
  -d '{"status":"in_progress"}'

# Assign
curl -s -X POST http://127.0.0.1:8000/api/issues/1/assign \
  -H 'Content-Type: application/json' \
  -d '{"assignee":"alex"}'

# Comment
curl -s -X POST http://127.0.0.1:8000/api/issues/1/comments \
  -H 'Content-Type: application/json' \
  -d '{"author":"alex","body":"Looks good"}'
```

## UI role toy

The HTML UI reads a toy role from the `ff_role` cookie (or `X-User-Role` header): `admin` \| `user`. Use the header switcher to flip roles. Non-admins do not see admin controls (status / assign / delete). The REST API does **not** enforce that role — that mismatch is intentional.

Trainers: see [SECURITY_LAB.md](SECURITY_LAB.md).

## Layout

```
app/           FastAPI app (API + Jinja routes + SQLite helpers)
templates/     Thin HTML UI
static/        Minimal CSS
requirements.txt
SECURITY_LAB.md
```

## Notes

- Persistence: SQLite file `featureflow.db` (created on first start; gitignored).
- No JWT / OAuth — roles are a demo cookie/header only.
- Almost no automated tests on purpose (day-2 lab material).
