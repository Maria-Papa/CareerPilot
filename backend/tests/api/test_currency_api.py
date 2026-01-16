from typing import Callable

import pytest
from app.models import Currency
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import (
    assert_404,
    assert_list,
    assert_status,
)

pytestmark = pytest.mark.integration


def test_create_and_get_currency(client: TestClient, db_session: Session) -> None:
    payload = {
        "code": "EUR",
        "symbol": "€",
    }

    resp = client.post("/currencies", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    cur_id = data["id"]

    resp = client.get(f"/currencies/{cur_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == cur_id


def test_list_currencies(
    client: TestClient,
    db_session: Session,
    currency_factory: Callable[..., Currency],
) -> None:
    currency_factory(code="EUR")
    currency_factory(code="USD")

    resp = client.get("/currencies")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_currency(
    client: TestClient,
    db_session: Session,
    currency_factory: Callable[..., Currency],
) -> None:
    cur = currency_factory(code="EUR", symbol="€")
    payload = {"symbol": "€€"}

    resp = client.patch(f"/currencies/{cur.id}", json=payload)
    assert_status(resp, 200)
    assert resp.json()["symbol"] == "€€"

    db_session.refresh(cur)
    assert cur.symbol == "€€"


def test_delete_currency(
    client: TestClient,
    db_session: Session,
    currency_factory: Callable[..., Currency],
) -> None:
    cur = currency_factory(code="EUR")

    resp = client.delete(f"/currencies/{cur.id}")
    assert_status(resp, 204)

    resp = client.get(f"/currencies/{cur.id}")
    assert_404(resp)
