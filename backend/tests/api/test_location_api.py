from typing import Callable

import pytest
from app.models import Location
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import (
    assert_404,
    assert_list,
    assert_status,
)

pytestmark = pytest.mark.integration


def test_create_and_get_location(client: TestClient, db_session: Session) -> None:
    payload = {
        "name": "Athens",
        "country_code": "GR",
        "currency_id": 1,
    }

    resp = client.post("/locations", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    loc_id = data["id"]

    resp = client.get(f"/locations/{loc_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == loc_id


def test_list_locations(
    client: TestClient, db_session: Session, location_factory: Callable[..., Location]
) -> None:
    location_factory(name="Thessaloniki")
    location_factory(name="Stockholm")

    resp = client.get("/locations")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_location(
    client: TestClient, db_session: Session, location_factory: Callable[..., Location]
) -> None:
    loc = location_factory(name="OldName")
    payload = {"name": "NewName"}

    resp = client.patch(f"/locations/{loc.id}", json=payload)
    assert_status(resp, 200)
    assert resp.json()["name"] == "NewName"

    db_session.refresh(loc)
    assert loc.name == "NewName"


def test_delete_location(
    client: TestClient, db_session: Session, location_factory: Callable[..., Location]
) -> None:
    loc = location_factory()

    resp = client.delete(f"/locations/{loc.id}")
    assert_status(resp, 204)

    resp = client.get(f"/locations/{loc.id}")
    assert_404(resp)
