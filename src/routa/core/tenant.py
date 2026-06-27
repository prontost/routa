"""Мультиюзер: пользователи (тенанты) + текущий тенант запроса.

Данные пользователей теперь живут в единой БД Avalone (`avalone_core.db`).
Routa работает с таблицами `users` и `admins` через `UserRepository`;
администраторы Work отмечены в `admins` с `module='work'`.

Все функции модуля оставлены для обратной совместимости и делегируют методам
единого инстанса `TenantService`.
"""

from __future__ import annotations

from contextvars import ContextVar

from avalone_core.database import Service
from avalone_core import glossary_db as glossary
from routa.core.user_repository import UserRepository
from routa.core.db import DB_PATH  # noqa: F401  # backward-compatible re-export

# текущий тенант запроса; 0 = не установлен (запрещаем доступ к данным)
_current: ContextVar[int] = ContextVar("tenant_id", default=0)

OWNER_TENANT_ID = 1  # владелец (его данные переносятся при миграции)


class TenantService(Service):
    """Tenant/user business logic and request-scoped tenant context."""

    def __init__(self, repository: UserRepository | None = None) -> None:
        self._repo = repository or UserRepository()

    # --- контекст текущего тенанта ---
    def set_current(self, tenant_id: int) -> None:
        _current.set(tenant_id)

    def current(self) -> int:
        return _current.get()

    def require_current(self) -> int:
        t = _current.get()
        if not t:
            raise PermissionError(glossary.t("error_tenant_not_set", lang="ru"))
        return t

    # --- аутентификация ---
    def authenticate(self, login: str, password: str) -> int | None:
        u = self._repo.get_by_login(login)
        if u and self._repo.verify_password(password, u["pwhash"]):
            return u["id"]
        return None

    def create_user(self, login: str, password: str, email: str = "") -> int:
        return self._repo.create(login, password, email)

    def login_taken(self, login: str) -> bool:
        return self._repo.login_taken(login)

    def count_users(self) -> int:
        return self._repo.count_users()

    def count_entries(self) -> int:
        """Admin aggregate: total entries across all tenants."""
        return self._repo.count_entries()

    def all_ids(self) -> list[int]:
        return self._repo.all_ids()

    def list_users(self) -> list[dict]:
        """Admin aggregate: all users with entry counts."""
        return self._repo.list_users()

    def get_user(self, tenant_id: int) -> dict | None:
        return self._repo.get_user(tenant_id)

    def get_user_by_login(self, login: str) -> dict | None:
        return self._repo.get_user_by_login(login)

    def accounts_for_email(self, email: str) -> list[dict]:
        return self._repo.accounts_for_email(email)

    def change_password(self, tenant_id: int, old_pw: str, new_pw: str) -> bool:
        return self._repo.change_password(tenant_id, old_pw, new_pw)

    def set_password(self, tenant_id: int, new_pw: str) -> None:
        self._repo.set_password(tenant_id, new_pw)

    def set_email(self, tenant_id: int, email: str) -> None:
        self._repo.set_email(tenant_id, email)

    def set_verify_code(self, tenant_id: int, code: str) -> None:
        self._repo.set_verify_code(tenant_id, code)

    def check_verify_code(self, tenant_id: int, code: str) -> bool:
        return self._repo.check_verify_code(tenant_id, code)

    def set_reset_token(self, tenant_id: int, token: str, expires_iso: str) -> None:
        self._repo.set_reset_token(tenant_id, token, expires_iso)

    def consume_reset_token(self, token: str) -> int | None:
        return self._repo.consume_reset_token(token)

    def delete_user(self, tenant_id: int) -> None:
        self._repo.delete_user(tenant_id)

    def ensure_owner(self, login: str, password: str) -> int:
        return self._repo.ensure_owner(login, password)

    # --- администраторы ---
    def ensure_admin_table(self) -> None:
        self._repo.ensure_admin_table()

    def ensure_admin(self) -> None:
        """Backward-compatible alias for ensure_admin_table."""
        self.ensure_admin_table()

    def is_admin(self, user_id: int | None) -> bool:
        return self._repo.is_admin(user_id)

    def list_admins(self) -> list[dict]:
        return self._repo.list_admins()

    def add_admin(self, user_id: int) -> None:
        self._repo.add_admin(user_id)

    def remove_admin(self, user_id: int) -> None:
        self._repo.remove_admin(user_id)


# --- backward-compatible module-level API ---
_default_service = TenantService()
_default_repo = _default_service._repo

set_current = _default_service.set_current
current = _default_service.current
require_current = _default_service.require_current
authenticate = _default_service.authenticate
create_user = _default_service.create_user
login_taken = _default_service.login_taken
count_users = _default_service.count_users
count_entries = _default_service.count_entries
all_ids = _default_service.all_ids
get_user = _default_service.get_user
get_user_by_login = _default_service.get_user_by_login
accounts_for_email = _default_service.accounts_for_email
change_password = _default_service.change_password
set_password = _default_service.set_password
set_email = _default_service.set_email
set_verify_code = _default_service.set_verify_code
check_verify_code = _default_service.check_verify_code
set_reset_token = _default_service.set_reset_token
consume_reset_token = _default_service.consume_reset_token
delete_user = _default_service.delete_user
ensure_owner = _default_service.ensure_owner
ensure_admin_table = _default_service.ensure_admin_table
ensure_admin = _default_service.ensure_admin
is_admin = _default_service.is_admin
list_admins = _default_service.list_admins
add_admin = _default_service.add_admin
remove_admin = _default_service.remove_admin
hash_password = _default_repo.hash_password
verify_password = _default_repo.verify_password
get_by_login = _default_repo.get_by_login
_conn = _default_repo._conn
