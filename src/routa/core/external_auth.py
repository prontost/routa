"""Avalone SSO integration: shared signed cookie across avalone.online domain.

Avalone issues `avalone_session` cookie. Routa reads it, verifies the signature
with the shared key, and maps the Avalone user_id to a local tenant.
"""

import sqlite3
from datetime import datetime, timezone

from fastapi import Request
from itsdangerous import URLSafeSerializer

from routa.core import tenant
from routa.core.config import settings

_EXTERNAL_SCHEMA = """
CREATE TABLE IF NOT EXISTS external_users (
    provider    TEXT NOT NULL,
    external_id TEXT NOT NULL,
    tenant_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TEXT NOT NULL,
    PRIMARY KEY (provider, external_id)
);
"""

_signer = URLSafeSerializer(
    settings().avalone_fernet_key or settings().fernet_key,
    salt="avalone-session",
)


def _conn() -> sqlite3.Connection:
    from routa.core.db import DB_PATH

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(_EXTERNAL_SCHEMA)
    return con


def user_id_of(request: Request) -> int:
    """Return Avalone user_id from cookie, or 0 if missing/invalid."""
    token = request.cookies.get(settings().avalone_cookie_name)
    if not token:
        return 0
    try:
        return int(_signer.loads(token))
    except Exception:
        return 0


def get_tenant_id(external_user_id: int) -> int | None:
    """Map Avalone user_id to local tenant_id."""
    with _conn() as con:
        r = con.execute(
            "SELECT tenant_id FROM external_users WHERE provider='avalone' AND external_id=?",
            (str(external_user_id),),
        ).fetchone()
    if r:
        return int(r[0])
    return None


def _create_mapping(external_user_id: int, tenant_id: int) -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _conn() as con:
        con.execute(
            "INSERT OR REPLACE INTO external_users (provider, external_id, tenant_id, created_at) VALUES (?, ?, ?, ?)",
            ("avalone", str(external_user_id), tenant_id, now),
        )


def get_or_create_tenant(external_user_id: int) -> int:
    """Return local tenant_id for Avalone user, creating both mapping and user if needed."""
    tid = get_tenant_id(external_user_id)
    if tid:
        return tid

    login = f"avalone_{external_user_id}"
    if tenant.login_taken(login):
        u = tenant.get_by_login(login)
        tid = u["id"]
    else:
        import secrets

        tid = tenant.create_user(login, secrets.token_urlsafe(32))

    _create_mapping(external_user_id, tid)
    return tid
