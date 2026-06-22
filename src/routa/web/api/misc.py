"""Routa API domain router."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from routa.core import notify, security

log = logging.getLogger(__name__)
router = APIRouter()


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return (fwd.split(",")[0].strip() if fwd
            else (request.client.host if request.client else "?"))


@router.get("/me")
async def me():
    """Current user profile (for the PWA banner)."""
    from routa.core import tenant
    tid = tenant.require_current()
    u = tenant.get_user(tid)
    if not u:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return {"login": u["login"], "email": u["email"],
            "email_verified": u["email_verified"], "is_admin": tenant.is_admin(tid)}

@router.post("/send-verify-code")
async def send_verify_code(request: Request):
    """Send (or resend) a 6-digit email verification code. Rate-limited."""
    from routa.core import tenant
    ip = _client_ip(request)
    if not security.allow_verify(ip):
        return JSONResponse({"error": "rate_limit"}, status_code=429)
    tid = tenant.require_current()
    u = tenant.get_user(tid)
    if not u or not u.get("email"):
        return JSONResponse({"error": "no_email"}, status_code=400)
    code = security.new_code()
    tenant.set_verify_code(tid, code)
    body = (
        f"Код подтверждения email для Routa: {code}\n\n"
        f"Код действует 30 минут. Если вы не запрашивали подтверждение — просто проигнорируйте письмо."
    )
    ok = notify._send_email(u["email"], "Подтверждение email", body)
    return {"sent": ok}

@router.post("/verify-email")
async def verify_email(request: Request, payload: dict):
    """Verify the 6-digit code sent by email."""
    from routa.core import tenant
    ip = _client_ip(request)
    if not security.allow_verify(ip):
        return JSONResponse({"error": "rate_limit"}, status_code=429)
    tid = tenant.require_current()
    code = str(payload.get("code", "")).strip()
    if tenant.check_verify_code(tid, code):
        return {"verified": True}
    return JSONResponse({"error": "invalid_code"}, status_code=400)
