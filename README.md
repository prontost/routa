# Work — Avalone

Organize work trips and commutes inside the Avalone platform. Live at `https://work.avalone.online`.

Work is the first active branch of Avalone. It is built on the shared Avalone shell so users never feel like they left the platform when switching between Work, Counta, and the portal.

- **Trips** — create, edit, close, and delete rides to/from work.
- **Invites** — share a trip via link or QR; colleagues join with one click using Avalone SSO.
- **Roles** — driver, passenger, or not going; anyone can change their role freely.
- **Stats** — per-user and global trip statistics with simple charts.
- **Notifications** — in-app and email reminders about invites, role changes, and upcoming trips.
- **Avalone SSO** — shared `.avalone.online` session cookie; sign in once across all apps.

## Stack

- Python ≥3.13, managed with `uv`
- FastAPI + Uvicorn
- SQLite (`~/.routa/routa.db`; override with `ROUTA_DB_PATH`)
- Jinja2 + vanilla JS SPA
- Shared Avalone shell (`avalone-shell.css`, `avalone-shell.js`, `shell.html`)
- `itsdangerous` signed session cookies + Fernet-signed Avalone SSO cookie
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

Open `http://127.0.0.1:8812`.

For cross-app SSO locally you need a shared domain; the production setup uses Cloudflare Tunnels so `avalone.online`, `counta.avalone.online`, and `work.avalone.online` all share the `avalone_session` cookie.

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
