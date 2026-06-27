"""Global (instance-wide) settings stored in SQLite.

Per-tenant settings live in notify.user_settings. These settings affect the
whole instance and are writable by instance admins.

Backward-compatible facade: module-level `get`, `set`, `get_all`, and `DEFAULTS`
remain and delegate to the default `GlobalSettingsService` instance.
"""

from routa.core.global_settings_repository import DEFAULTS, GlobalSettingsRepository
from routa.core.global_settings_service import GlobalSettingsService

# --- backward-compatible module-level API ---
_default_service = GlobalSettingsService()

get = _default_service.get
set = _default_service.set
get_all = _default_service.get_all

__all__ = [
    "DEFAULTS",
    "GlobalSettingsRepository",
    "GlobalSettingsService",
    "get",
    "set",
    "get_all",
]
