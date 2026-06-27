"""Notifications API."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routa.core import notifications

router = APIRouter()


def _err(msg: str, code: int = 400):
    return JSONResponse({"error": msg}, status_code=code)


@router.get("/notifications")
async def list_notifications(limit: int = 50):
    try:
        return {"notifications": notifications.list_work_notifications(limit)}
    except PermissionError:
        return _err("error_unauthorized", 401)


@router.get("/notifications/unread-count")
async def unread_count():
    try:
        return {"count": notifications.unread_count()}
    except PermissionError:
        return _err("error_unauthorized", 401)


@router.post("/notifications/{notification_id}/read")
async def mark_read(notification_id: int):
    try:
        notifications.mark_read(notification_id)
        return {"ok": True}
    except PermissionError:
        return _err("error_unauthorized", 401)


@router.post("/notifications/read-all")
async def mark_all_read():
    try:
        notifications.mark_all_read()
        return {"ok": True}
    except PermissionError:
        return _err("error_unauthorized", 401)
