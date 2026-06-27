"""Authentication guards: rate limits, verification codes, reset tokens.

Rate-limit is an in-memory sliding window per key (ip|login). Good enough for a
single uvicorn process. Replace with Redis if we ever scale horizontally.
"""

import secrets
import time
from collections import defaultdict, deque

from routa.core import constants

_hits: dict[str, deque] = defaultdict(deque)


def _allow(key: str, limit: int | None = None, window: int | None = None) -> bool:
    if limit is None:
        limit = 10
    if window is None:
        window = constants.get("rate_limit_window_sec")
    now = time.time()
    dq = _hits[key]
    while dq and dq[0] < now - window:
        dq.popleft()
    if len(dq) >= limit:
        return False
    dq.append(now)
    return True


def allow_login(ip: str, login: str) -> bool:
    return _allow(f"login:{ip}:{login.lower()}", constants.get("max_login_attempts"))


def allow_register(ip: str) -> bool:
    return _allow(f"reg:{ip}", constants.get("max_register_attempts"))


def allow_verify(ip: str) -> bool:
    return _allow(f"vrf:{ip}", constants.get("max_verify_attempts"))


def allow_recover(ip: str) -> bool:
    return _allow(f"rec:{ip}", constants.get("max_recover_attempts"))


def new_code() -> str:
    """6-digit email verification code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def new_token() -> str:
    """One-time password-reset token (URL-safe)."""
    return secrets.token_urlsafe(constants.get("password_reset_token_entropy"))


def validate_password(password: str, strict: bool = False) -> tuple[bool, str]:
    """Validate password complexity. Returns (ok, error_key).

    Non-strict (default): only minimum length from constants.
    Strict: ≥8 chars, uppercase, lowercase, digit, special character.
    """
    import re
    if not password:
        return False, "error_password_empty"
    min_len = constants.get("min_password_length")
    if not strict:
        if len(password) < min_len:
            return False, "error_password_too_short"
        return True, ""
    if len(password) < 8:
        return False, "error_password_too_short"
    if not re.search(r"[A-ZА-Я]", password):
        return False, "error_password_no_upper"
    if not re.search(r"[a-zа-я]", password):
        return False, "error_password_no_lower"
    if not re.search(r"\d", password):
        return False, "error_password_no_digit"
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False, "error_password_no_special"
    return True, ""
