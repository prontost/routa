"""Доступ пользователей к приложениям платформы."""
import pytest


@pytest.fixture
def app_access(tmp_path, monkeypatch):
    import routa.core.db as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "t.db")
    import importlib
    import routa.core.tenant as tenant
    import routa.core.app_access as app_access
    importlib.reload(tenant)
    importlib.reload(app_access)
    return app_access, tenant


def test_default_public_app_accessible(app_access):
    aa, tenant = app_access
    tid = tenant.create_user("u1", "pw")
    assert "routa" in aa.list_for_user(tid)
    assert aa.is_accessible(tid, "routa") is True


def test_admin_can_revoke_access(app_access):
    aa, tenant = app_access
    tid = tenant.create_user("u2", "pw")
    aa.set_access(tid, "routa", False)
    assert "routa" not in aa.list_for_user(tid)
    assert aa.is_accessible(tid, "routa") is False
    aa.set_access(tid, "routa", True)
    assert aa.is_accessible(tid, "routa") is True


def test_unknown_app_raises(app_access):
    aa, tenant = app_access
    tid = tenant.create_user("u3", "pw")
    with pytest.raises(ValueError):
        aa.set_access(tid, "nonexistent", True)


def test_grant_default_creates_rows(app_access):
    aa, tenant = app_access
    tid = tenant.create_user("u4", "pw")
    aa.grant_default(tid)
    admin_view = aa.list_for_admin(tid)
    routa = next(a for a in admin_view if a["id"] == "routa")
    assert routa["enabled"] is True
