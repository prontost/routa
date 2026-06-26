import os

import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "routa_test.db"
    os.environ["ROUTA_DB_PATH"] = str(db_path)
    from routa.core import db, tenant
    from routa.web.app import app
    from fastapi.testclient import TestClient

    import routa.core.rides as rides_mod
    import routa.core.tenant as tenant_mod
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(rides_mod, "DB_PATH", db_path)
    monkeypatch.setattr(tenant_mod, "DB_PATH", db_path)

    tenant.ensure_owner("owner", "owner-pass-123")
    tenant.set_current(1)
    yield TestClient(app)


def test_create_and_get_trip(client):
    from routa.core import rides

    trip = rides.create_trip("to_work", "2026-06-30", "08:00", comment="morning")
    assert trip["direction"] == "to_work"
    assert trip["trip_date"] == "2026-06-30"
    fetched = rides.get_trip(trip["id"])
    assert fetched["invite_code"]
    assert fetched["comment"] == "morning"


def test_list_trips_empty(client):
    from routa.core import rides

    trips = rides.list_trips()
    assert trips == []


def test_join_and_change_role(client):
    from routa.core import rides, tenant

    trip = rides.create_trip("from_work", "2026-06-30", "18:00")
    rides.join_trip(trip["id"], role="passenger")
    members = rides.get_trip(trip["id"])["members"]
    assert len(members) == 1
    assert members[0]["role"] == "passenger"

    rides.update_member(trip["id"], tenant.current(), "driver", 0)
    members = rides.get_trip(trip["id"])["members"]
    assert members[0]["role"] == "driver"


def test_trip_stats(client):
    from routa.core import rides

    rides.create_trip("to_work", "2026-06-30", "08:00")
    rides.create_trip("from_work", "2026-07-01", "18:00")
    stats = rides.stats()
    assert stats["total"] == 2


def test_api_list_trips_unauthorized(client):
    from routa.core import tenant

    tenant.set_current(0)
    resp = client.get("/api/trips")
    assert resp.status_code == 401


def test_api_version_is_open(client):
    resp = client.get("/api/version")
    assert resp.status_code == 200
