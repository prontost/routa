"""API for ride coordination MVP."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from routa.core import rides, tenant

router = APIRouter()


@router.get("/trips")
async def list_trips():
    try:
        return {"trips": rides.list_trips()}
    except PermissionError:
        return JSONResponse({"error": "unauthorized"}, status_code=401)


@router.post("/trips")
async def create_trip(request: Request):
    try:
        data = await request.json()
        trip = rides.create_trip(
            direction=data.get("direction", "to_work"),
            trip_date=data.get("date", ""),
            trip_time=data.get("time", ""),
        )
        return {"trip": trip}
    except PermissionError:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/trips/{trip_id}")
async def get_trip(trip_id: int):
    trip = rides.get_trip(trip_id)
    if not trip:
        return JSONResponse({"error": "not found"}, status_code=404)
    return {"trip": trip}


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
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


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
        return JSONResponse({"error": "unauthorized"}, status_code=403)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/trips/{trip_id}/close")
async def close_trip(trip_id: int):
    try:
        trip = rides.close_trip(trip_id)
        return {"trip": trip}
    except PermissionError:
        return JSONResponse({"error": "forbidden"}, status_code=403)
