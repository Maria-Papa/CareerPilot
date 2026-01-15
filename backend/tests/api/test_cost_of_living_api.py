from typing import Callable

import pytest
from app.models import Location
from app.models.cost_of_living import CostOfLiving
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import (
    assert_404,
    assert_list,
    assert_status,
)

pytestmark = pytest.mark.integration


def test_create_and_get_cost(
    client: TestClient, location_factory: Callable[..., Location]
) -> None:
    location = location_factory()

    payload = {
        "location_id": location.id,
        "yearly_cost": 123456,
        "title": "Test COL",
    }

    resp = client.post("/cost-of-living", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    col_id = data["id"]

    resp = client.get(f"/cost-of-living/{col_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == col_id


def test_list_costs(
    client: TestClient,
    db_session: Session,
    cost_of_living_factory: Callable[..., CostOfLiving],
) -> None:
    cost_of_living_factory(location_id=1, yearly_cost=100000)
    cost_of_living_factory(location_id=2, yearly_cost=200000)

    resp = client.get("/cost-of-living")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_cost(
    client: TestClient,
    db_session: Session,
    cost_of_living_factory: Callable[..., CostOfLiving],
) -> None:
    col = cost_of_living_factory(yearly_cost=100000)
    payload = {"yearly_cost": 150000}

    resp = client.patch(f"/cost-of-living/{col.id}", json=payload)
    assert_status(resp, 200)
    assert resp.json()["yearly_cost"] == 150000

    db_session.refresh(col)
    assert col.yearly_cost == 150000


def test_delete_cost(
    client: TestClient,
    db_session: Session,
    cost_of_living_factory: Callable[..., CostOfLiving],
) -> None:
    col = cost_of_living_factory()

    resp = client.delete(f"/cost-of-living/{col.id}")
    assert_status(resp, 204)

    resp = client.get(f"/cost-of-living/{col.id}")
    assert_404(resp)
