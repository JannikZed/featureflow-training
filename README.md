# FeatureFlow Training

Brownfield starter for the 2026 Copilot / Agents training.

**This is a training starter — intentionally imperfect.** It ships with a thin HTML UI and a SQLite-backed REST API. There is **no ready test suite** — you add tests during the labs. Do not use it in production.

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

Or with Make:

```bash
make install
make run
```

Open http://127.0.0.1:8000/ for the UI. Interactive API docs: http://127.0.0.1:8000/docs

## What is FeatureFlow?

A minimal issues tracker:

| Field | Notes |
|-------|--------|
| `id` | integer PK |
| `title` | required |
| `description` | free text |
| `status` | `open` \| `in_progress` \| `done` |
| `assignee` | optional |
| `created_at` | set on create |

Comments hang off issues. The HTML UI and REST API share the same SQLite database (`featureflow.db`, created on first start, gitignored).

## Quick API smoke checks

```bash
# Create an issue
curl -s -X POST http://127.0.0.1:8000/api/issues \
  -H 'Content-Type: application/json' \
  -d '{"title":"Dark mode","description":"Theme toggle","status":"open"}'

# List issues
curl -s http://127.0.0.1:8000/api/issues

# Comment
curl -s -X POST http://127.0.0.1:8000/api/issues/1/comments \
  -H 'Content-Type: application/json' \
  -d '{"author":"alex","body":"Looks good"}'
```

Explore further endpoints via `/docs`.

## UI role switcher

The HTML UI reads a toy role from the `ff_role` cookie (or `X-User-Role` header): `admin` \| `user`. Use the header switcher to flip roles and see how the UI changes. Roles are a demo convenience only — there is no JWT/OAuth.

## Layout

```
app/              FastAPI app (API + Jinja routes + SQLite helpers)
templates/        Thin HTML UI
static/           Minimal CSS
Makefile          install / run helpers
requirements.txt
```

## Tests

**Tests are not included in this starter.** You build them in the labs:

- Tag 1 — Spec-Driven Lab 4
- Tag 2 — Test-Agent / run-tests

`make test-*` targets exist only as placeholders and exit with a short reminder until you add a suite.

## Notes

- Persistence: SQLite file `featureflow.db` (gitignored).
- You will add project context files (for example `AGENTS.md`) and tests during the labs — start from this brownfield tree as-is.
