"""Avalone SSO integration: shared signed cookie across avalone.online domain.

Avalone issues `avalone_session` cookie. Work reads it, verifies the signature
with the shared key, and uses the Avalone user_id directly as the Work tenant_id.
"""

from fastapi import Request
from itsdangerous import URLSafeSerializer

from routa.core.config import settings

_signer = URLSafeSerializer(
    settings().avalone_fernet_key or settings().fernet_key,
    salt="avalone-session",
)


def user_id_of(request: Request) -> int:
    """Return Avalone user_id from cookie, or 0 if missing/invalid."""
    token = request.cookies.get(settings().avalone_cookie_name)
    if not token:
        return 0
    try:
        return int(_signer.loads(token))
    except Exception:
        return 0


def get_user_id(request: Request) -> int:
    """Alias for user_id_of."""
    return user_id_of(request)
