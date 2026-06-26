"""Ride coordination for Work: work_trips, members, invitations, stats."""

import secrets
import sqlite3
from datetime import datetime, timezone

from routa.core import tenant
from routa.core.db import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS work_trips (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   INTEGER NOT NULL,
    direction   TEXT NOT NULL CHECK(direction IN ('to_work','from_work')),
    trip_date   TEXT NOT NULL,
    trip_time   TEXT NOT NULL,
    comment     TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','closed','cancelled')),
    invite_code TEXT UNIQUE NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS work_trip_members (
    trip_id     INTEGER NOT NULL REFERENCES work_trips(id) ON DELETE CASCADE,
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
    # Migration: add comment column if missing (older DBs)
    cols = [r[1] for r in con.execute("PRAGMA table_info(work_trips)").fetchall()]
    if "comment" not in cols:
        con.execute("ALTER TABLE work_trips ADD COLUMN comment TEXT DEFAULT ''")
    return con


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _generate_code() -> str:
    return secrets.token_urlsafe(12)


def create_trip(direction: str, trip_date: str, trip_time: str, comment: str = "") -> dict:
    tid = tenant.require_current()
    code = _generate_code()
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO work_trips (tenant_id, direction, trip_date, trip_time, comment, invite_code, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tid, direction, trip_date, trip_time, comment.strip(), code, _now()),
        )
        trip_id = cur.lastrowid
        con.execute(
            "INSERT INTO work_trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, tid, "unknown", 0, _now()),
        )
    return get_trip(trip_id)


def update_trip(trip_id: int, direction: str | None = None, trip_date: str | None = None,
                trip_time: str | None = None, comment: str | None = None,
                status: str | None = None) -> dict:
    tid = tenant.require_current()
    fields = []
    params = []
    if direction is not None:
        fields.append("direction=?"); params.append(direction)
    if trip_date is not None:
        fields.append("trip_date=?"); params.append(trip_date)
    if trip_time is not None:
        fields.append("trip_time=?"); params.append(trip_time)
    if comment is not None:
        fields.append("comment=?"); params.append(comment.strip())
    if status is not None:
        fields.append("status=?"); params.append(status)
    if not fields:
        return get_trip(trip_id)
    params.append(trip_id)
    with _conn() as con:
        trip = con.execute("SELECT tenant_id FROM work_trips WHERE id=?", (trip_id,)).fetchone()
        if not trip or trip["tenant_id"] != tid:
            raise PermissionError("only creator can edit")
        con.execute(f"UPDATE work_trips SET {', '.join(fields)} WHERE id=?", params)
    return get_trip(trip_id)


def delete_trip(trip_id: int) -> None:
    tid = tenant.require_current()
    with _conn() as con:
        trip = con.execute("SELECT tenant_id FROM work_trips WHERE id=?", (trip_id,)).fetchone()
        if not trip or trip["tenant_id"] != tid:
            raise PermissionError("only creator can delete")
        con.execute("DELETE FROM work_trips WHERE id=?", (trip_id,))


def get_trip(trip_id: int) -> dict | None:
    with _conn() as con:
        row = con.execute("SELECT * FROM work_trips WHERE id=?", (trip_id,)).fetchone()
        if not row:
            return None
        return _trip_with_members(con, dict(row))


def get_trip_by_code(invite_code: str) -> dict | None:
    with _conn() as con:
        row = con.execute("SELECT * FROM work_trips WHERE invite_code=?", (invite_code,)).fetchone()
        if not row:
            return None
        return _trip_with_members(con, dict(row))


def _trip_with_members(con: sqlite3.Connection, trip: dict) -> dict:
    members = [
        dict(r)
        for r in con.execute(
            "SELECT tm.*, u.login FROM work_trip_members tm JOIN users u ON u.id=tm.tenant_id WHERE tm.trip_id=? ORDER BY tm.updated_at",
            (trip["id"],),
        ).fetchall()
    ]
    trip["members"] = members
    return trip


def list_trips(filter_status: str = "all", direction: str | None = None,
               only_mine: bool = False, limit: int = 100) -> list[dict]:
    tid = tenant.require_current()
    conditions = ["t.id IN (SELECT trip_id FROM work_trip_members WHERE tenant_id=?)"]
    params: list = [tid]
    if filter_status == "upcoming":
        conditions.append("t.trip_date >= date('now')")
    elif filter_status == "past":
        conditions.append("t.trip_date < date('now')")
    elif filter_status == "open":
        conditions.append("t.status = 'open'")
    elif filter_status == "closed":
        conditions.append("t.status = 'closed'")
    if direction:
        conditions.append("t.direction = ?"); params.append(direction)
    if only_mine:
        conditions.append("t.tenant_id = ?"); params.append(tid)
    where = " AND ".join(conditions)
    params.append(limit)
    with _conn() as con:
        rows = con.execute(
            f"SELECT t.* FROM work_trips t WHERE {where} ORDER BY t.trip_date, t.trip_time LIMIT ?",
            params,
        ).fetchall()
        return [_trip_with_members(con, dict(r)) for r in rows]


def join_trip(trip_id: int, role: str = "unknown", seats: int = 0) -> dict:
    tid = tenant.require_current()
    with _conn() as con:
        trip = con.execute("SELECT id, status FROM work_trips WHERE id=?", (trip_id,)).fetchone()
        if not trip:
            raise ValueError("trip not found")
        if trip["status"] != "open":
            raise ValueError("trip is closed or cancelled")
        con.execute(
            "INSERT OR REPLACE INTO work_trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, tid, role, seats, _now()),
        )
    return get_trip(trip_id)


def join_trip_by_code(invite_code: str, role: str = "unknown", seats: int = 0) -> dict:
    with _conn() as con:
        row = con.execute("SELECT id FROM work_trips WHERE invite_code=?", (invite_code,)).fetchone()
        if not row:
            raise ValueError("invalid invite code")
        trip_id = row["id"]
    return join_trip(trip_id, role, seats)


def leave_trip(trip_id: int) -> None:
    tid = tenant.require_current()
    with _conn() as con:
        con.execute("DELETE FROM work_trip_members WHERE trip_id=? AND tenant_id=?", (trip_id, tid))


def update_member(trip_id: int, member_tid: int, role: str, seats: int = 0) -> dict:
    """Any member can update any other member's status (equal rights)."""
    current_tid = tenant.require_current()
    with _conn() as con:
        is_member = con.execute(
            "SELECT 1 FROM work_trip_members WHERE trip_id=? AND tenant_id=?",
            (trip_id, current_tid),
        ).fetchone()
        if not is_member:
            raise PermissionError("not a member of this trip")
        con.execute(
            "INSERT OR REPLACE INTO work_trip_members (trip_id, tenant_id, role, seats, updated_at) VALUES (?, ?, ?, ?, ?)",
            (trip_id, member_tid, role, seats, _now()),
        )
    return get_trip(trip_id)


def close_trip(trip_id: int) -> dict:
    return update_trip(trip_id, status="closed")


def reopen_trip(trip_id: int) -> dict:
    return update_trip(trip_id, status="open")


# Stats

def stats(period: str = "all") -> dict:
    """Return aggregated ride statistics for the current user."""
    tid = tenant.require_current()
    date_filter = ""
    params = [tid]
    if period == "week":
        date_filter = "AND t.trip_date >= date('now', '-7 days')"
    elif period == "month":
        date_filter = "AND t.trip_date >= date('now', '-30 days')"
    elif period == "year":
        date_filter = "AND t.trip_date >= date('now', '-365 days')"
    with _conn() as con:
        total = con.execute(
            f"SELECT COUNT(*) FROM work_trip_members tm JOIN work_trips t ON t.id=tm.trip_id WHERE tm.tenant_id=? {date_filter}",
            params,
        ).fetchone()[0]
        as_driver = con.execute(
            f"SELECT COUNT(*) FROM work_trip_members tm JOIN work_trips t ON t.id=tm.trip_id WHERE tm.tenant_id=? AND tm.role='driver' {date_filter}",
            params,
        ).fetchone()[0]
        as_passenger = con.execute(
            f"SELECT COUNT(*) FROM work_trip_members tm JOIN work_trips t ON t.id=tm.trip_id WHERE tm.tenant_id=? AND tm.role='passenger' {date_filter}",
            params,
        ).fetchone()[0]
        by_day = [
            dict(r)
            for r in con.execute(
                f"SELECT t.trip_date as day, COUNT(*) as count FROM work_trip_members tm JOIN work_trips t ON t.id=tm.trip_id WHERE tm.tenant_id=? {date_filter} GROUP BY t.trip_date ORDER BY t.trip_date",
                params,
            ).fetchall()
        ]
        members_table = [
            dict(r)
            for r in con.execute(
                f"""SELECT u.login,
                           SUM(CASE WHEN tm.role='driver' THEN 1 ELSE 0 END) as driver_count,
                           SUM(CASE WHEN tm.role='passenger' THEN 1 ELSE 0 END) as passenger_count
                    FROM work_trip_members tm
                    JOIN work_trips t ON t.id=tm.trip_id
                    JOIN users u ON u.id=tm.tenant_id
                    WHERE t.id IN (SELECT trip_id FROM work_trip_members WHERE tenant_id=?) {date_filter}
                    GROUP BY tm.tenant_id
                    ORDER BY driver_count DESC, passenger_count DESC""",
                [tid] + ([] if not date_filter else []),
            ).fetchall()
        ]
    return {
        "total": total,
        "as_driver": as_driver,
        "as_passenger": as_passenger,
        "by_day": by_day,
        "members_table": members_table,
    }
