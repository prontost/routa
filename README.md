# Routa

Work-in-progress app for organizing people commute / work trips. Live at `https://routa.avalone.online`.

Currently the public UI is a placeholder: home and analytics show a "coming soon" card. The codebase was forked from Counta, so the backend still carries the double-entry ledger machinery while the product is being repurposed.

- **Own SQLite database** — no external accounting system, no ERPNext, no AI.
- **Standalone** — own login and DB; no built-in app switcher; SSO is a future direction, not implemented yet.
- **i18n-first** — `ru` / `en` / `ko` from a central glossary.
- **Forked from Counta** — accounts, journal and reports still exist in code but will be reworked into trip-management flows.

## Stack

- Python ≥3.13, managed with `uv`
- FastAPI + Uvicorn
- SQLite (`~/.routa/routa.db`; override with `ROUTA_DB_PATH`)
- Jinja2 + vanilla JS SPA
- `itsdangerous` signed session cookies
- pytest for tests

## Dev

```bash
uv sync
# Create .env from example and fill ROUTA_FERNET_KEY at minimum:
cp .env.example .env
# Optional: override SQLite path (default is ~/.routa/routa.db)
# export ROUTA_DB_PATH=/path/to/routa.db
uv run python scripts/pre_flight.py   # deploy gate
uv run uvicorn routa.web.app:app --host 127.0.0.1 --port 8812 --reload
```

Open `http://127.0.0.1:8810`.

## Tests

```bash
uv run pytest -q
```

## Deploy gate

Every change must pass:

```bash
uv run python scripts/pre_flight.py
```

This checks Python syntax, tests, i18n coverage, and inline JS syntax.

## Docs for agents

See `AGENTS.md` for architecture, patterns, and operating rules.
