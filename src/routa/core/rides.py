"""MVP ride coordination for Work: trips, members, invitations.

A trip is a single commute event (to work / from work) on a specific date.
Members mark themselves (or each other) as driver, passenger, or not going.
"""

import secrets
import sqlite3
from datetime import datetime, timezone

from routa.core import tenant
from routa.core.db import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS trips (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   INTEGER NOT NULL,
    direction   TEXT NOT NULL CHECK(direction IN ('to_work','from_work')),
    trip_date   TEXT NOT NULL,
    trip_time   TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','closed','cancelled')),
    invite_code TEXT UNIQUE NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trip_members (
    trip_id     INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    tenant_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role        TEXT NOT NULL CHECK(role IN ('driver','passenger','not_going','unknown')),
    seats       INTEGER NOT NULL DEFAULT 0,
    updated_at  TEXT NOT NULL,
    PRIMARY KEY (trip_id, tenant_id)
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


def _generate_code() -> str:
    return secrets.token_urlsafe(12)


def create_trip(direction: str, trip_date: str, trip_time: str) -> dict:
    tid = tenant.require_current()
    code = _generate_code()
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO trips (tenant_id, direction, trip_date, trip_time, invite_code, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (tid, direction, trip_date, trip_time, code, _now()),
        )
        trip_id = cur.lastrowid
        con.execute(
            "INSERT INTO trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, tid, "unknown", 0, _now()),
        )
    return get_trip(trip_id)


def get_trip(trip_id: int) -> dict | None:
    with _conn() as con:
        row = con.execute("SELECT * FROM trips WHERE id=?", (trip_id,)).fetchone()
        if not row:
            return None
        return _trip_with_members(con, dict(row))


def get_trip_by_code(invite_code: str) -> dict | None:
    with _conn() as con:
        row = con.execute("SELECT * FROM trips WHERE invite_code=?", (invite_code,)).fetchone()
        if not row:
            return None
        return _trip_with_members(con, dict(row))


def _trip_with_members(con: sqlite3.Connection, trip: dict) -> dict:
    members = [
        dict(r)
        for r in con.execute(
            "SELECT tm.*, u.login FROM trip_members tm JOIN users u ON u.id=tm.tenant_id WHERE tm.trip_id=? ORDER BY tm.updated_at",
            (trip["id"],),
        ).fetchall()
    ]
    trip["members"] = members
    return trip


def list_trips(limit: int = 50) -> list[dict]:
    tid = tenant.require_current()
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM trips WHERE id IN (SELECT trip_id FROM trip_members WHERE tenant_id=?) ORDER BY trip_date, trip_time LIMIT ?",
            (tid, limit),
        ).fetchall()
        return [_trip_with_members(con, dict(r)) for r in rows]


def join_trip(trip_id: int, role: str = "unknown", seats: int = 0) -> dict:
    tid = tenant.require_current()
    with _conn() as con:
        trip = con.execute("SELECT id FROM trips WHERE id=?", (trip_id,)).fetchone()
        if not trip:
            raise ValueError("trip not found")
        con.execute(
            "INSERT OR REPLACE INTO trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, tid, role, seats, _now()),
        )
    return get_trip(trip_id)


def join_trip_by_code(invite_code: str, role: str = "unknown", seats: int = 0) -> dict:
    with _conn() as con:
        row = con.execute("SELECT id FROM trips WHERE invite_code=?", (invite_code,)).fetchone()
        if not row:
            raise ValueError("invalid invite code")
        trip_id = row["id"]
    return join_trip(trip_id, role, seats)


def update_member(trip_id: int, member_tid: int, role: str, seats: int = 0) -> dict:
    """Any member can update any other member's status (equal rights)."""
    current_tid = tenant.require_current()
    with _conn() as con:
        # Current user must be a member of this trip.
        is_member = con.execute(
            "SELECT 1 FROM trip_members WHERE trip_id=? AND tenant_id=?",
            (trip_id, current_tid),
        ).fetchone()
        if not is_member:
            raise PermissionError("not a member of this trip")
        con.execute(
            "INSERT OR REPLACE INTO trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, member_tid, role, seats, _now()),
        )
    return get_trip(trip_id)


def close_trip(trip_id: int) -> dict:
    tid = tenant.require_current()
    with _conn() as con:
        trip = con.execute("SELECT tenant_id FROM trips WHERE id=?", (trip_id,)).fetchone()
        if not trip or trip["tenant_id"] != tid:
            raise PermissionError("only creator can close")
        con.execute("UPDATE trips SET status='closed' WHERE id=?", (trip_id,))
    return get_trip(trip_id)
