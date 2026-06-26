"""In-app work_notifications for Work."""

import sqlite3
from datetime import datetime, timezone

from routa.core.db import DB_PATH
from routa.core import tenant

_SCHEMA = """
CREATE TABLE IF NOT EXISTS work_notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   INTEGER NOT NULL,
    type        TEXT NOT NULL,
    title       TEXT NOT NULL,
    body        TEXT NOT NULL,
    data        TEXT DEFAULT '',
    is_read     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);
"""


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(_SCHEMA)
    return con


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def notify(tenant_id: int, type_: str, title: str, body: str, data: str = "") -> int:
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO work_notifications (tenant_id, type, title, body, data, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (tenant_id, type_, title, body, data, _now()),
        )
        return cur.lastrowid


def list_work_notifications(limit: int = 50) -> list[dict]:
    tid = tenant.require_current()
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM work_notifications WHERE tenant_id=? ORDER BY created_at DESC LIMIT ?",
            (tid, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def unread_count() -> int:
    tid = tenant.require_current()
    with _conn() as con:
        r = con.execute(
            "SELECT COUNT(*) FROM work_notifications WHERE tenant_id=? AND is_read=0", (tid,)
        ).fetchone()
        return r[0] if r else 0


def mark_read(notification_id: int) -> None:
    tid = tenant.require_current()
    with _conn() as con:
        con.execute(
            "UPDATE work_notifications SET is_read=1 WHERE id=? AND tenant_id=?", (notification_id, tid)
        )


def mark_all_read() -> None:
    tid = tenant.require_current()
    with _conn() as con:
        con.execute("UPDATE work_notifications SET is_read=1 WHERE tenant_id=?", (tid,))
