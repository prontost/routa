"""API for ride coordination."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from routa.core import rides

router = APIRouter()


def _err(msg: str, code: int = 400) -> JSONResponse:
    return JSONResponse({"error": msg}, status_code=code)


@router.get("/trips")
async def list_trips(filter_status: str = "all", direction: str | None = None, only_mine: bool = False):
    try:
        return {"trips": rides.list_trips(filter_status, direction, only_mine)}
    except PermissionError:
        return _err("unauthorized", 401)


@router.post("/trips")
async def create_trip(request: Request):
    try:
        data = await request.json()
        trip = rides.create_trip(
            direction=data.get("direction", "to_work"),
            trip_date=data.get("date", ""),
            trip_time=data.get("time", ""),
            comment=data.get("comment", ""),
        )
        return {"trip": trip}
    except PermissionError:
        return _err("unauthorized", 401)
    except ValueError as e:
        return _err(str(e))


@router.get("/trips/{trip_id}")
async def get_trip(trip_id: int):
    trip = rides.get_trip(trip_id)
    if not trip:
        return _err("not found", 404)
    return {"trip": trip}


@router.put("/trips/{trip_id}")
async def update_trip(trip_id: int, request: Request):
    try:
        data = await request.json()
        trip = rides.update_trip(
            trip_id,
            direction=data.get("direction"),
            trip_date=data.get("date"),
            trip_time=data.get("time"),
            comment=data.get("comment"),
            status=data.get("status"),
        )
        return {"trip": trip}
    except PermissionError:
        return _err("forbidden", 403)
    except ValueError as e:
        return _err(str(e))


@router.delete("/trips/{trip_id}")
async def delete_trip(trip_id: int):
    try:
        rides.delete_trip(trip_id)
        return {"ok": True}
    except PermissionError:
        return _err("forbidden", 403)


@router.post("/trips/{trip_id}/join")
async def join_trip(trip_id: int, request: Request):
    try:
        data = await request.json()
        trip = rides.join_trip(
            trip_id,
            role=data.get("role", "unknown"),
            seats=int(data.get("seats", 0) or 0),
        )
        return {"trip": trip}
    except PermissionError:
        return _err("unauthorized", 401)
    except ValueError as e:
        return _err(str(e))


@router.post("/trips/{trip_id}/leave")
async def leave_trip(trip_id: int):
    try:
        rides.leave_trip(trip_id)
        return {"ok": True}
    except PermissionError:
        return _err("unauthorized", 401)


@router.post("/trips/{trip_id}/members/{member_tid}")
async def update_member(trip_id: int, member_tid: int, request: Request):
    try:
        data = await request.json()
        trip = rides.update_member(
            trip_id,
            member_tid,
            role=data.get("role", "unknown"),
            seats=int(data.get("seats", 0) or 0),
        )
        return {"trip": trip}
    except PermissionError:
        return _err("forbidden", 403)
    except ValueError as e:
        return _err(str(e))


@router.post("/trips/{trip_id}/close")
async def close_trip(trip_id: int):
    try:
        trip = rides.close_trip(trip_id)
        return {"trip": trip}
    except PermissionError:
        return _err("forbidden", 403)


@router.post("/trips/{trip_id}/reopen")
async def reopen_trip(trip_id: int):
    try:
        trip = rides.reopen_trip(trip_id)
        return {"trip": trip}
    except PermissionError:
        return _err("forbidden", 403)


@router.get("/trips/by-code/{invite_code}")
async def get_trip_by_code(invite_code: str):
    trip = rides.get_trip_by_code(invite_code)
    if not trip:
        return _err("not found", 404)
    return {"trip": trip}


@router.get("/stats")
async def get_stats(period: str = "all"):
    try:
        return {"stats": rides.stats(period)}
    except PermissionError:
        return _err("unauthorized", 401)


@router.get("/stats/export.csv")
async def export_csv(period: str = "all"):
    try:
        data = rides.stats(period)
        lines = ["login,driver_count,passenger_count"]
        for row in data.get("members_table", []):
            lines.append(f"{row['login']},{row['driver_count']},{row['passenger_count']}")
        return PlainTextResponse("\n".join(lines), media_type="text/csv; charset=utf-8")
    except PermissionError:
        return _err("unauthorized", 401)
