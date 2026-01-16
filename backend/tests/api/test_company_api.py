from typing import Callable

import pytest
from app.models.company import Company
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_company(client: TestClient, db_session: Session) -> None:
    payload = {"name": "ApiCo", "website": "https://api.co", "industry": "API"}
    resp = client.post("/api/v1/companies", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    company_id = data["id"]

    resp = client.get(f"/api/v1/companies/{company_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == company_id


def test_list_companies_endpoint(
    client: TestClient,
    db_session: Session,
    company_factory: Callable[..., Company],
) -> None:
    company_factory(name="ListAPI1")
    company_factory(name="ListAPI2")

    resp = client.get("/api/v1/companies")
    assert_status(resp, 200)
    assert_list(resp)


def test_patch_company(
    client: TestClient,
    db_session: Session,
    company_factory: Callable[..., Company],
) -> None:
    c = company_factory(name="PatchMe")
    payload = {"name": "Patched"}

    resp = client.patch(f"/api/v1/companies/{c.id}", json=payload)
    assert_status(resp, 200)
    assert resp.json()["name"] == "Patched"

    db_session.refresh(c)
    assert c.name == "Patched"


def test_delete_and_restore_endpoints(
    client: TestClient,
    db_session: Session,
    company_factory: Callable[..., Company],
) -> None:
    c = company_factory(name="DeleteAPI")

    resp = client.delete(f"/api/v1/companies/{c.id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/companies/{c.id}")
    assert_404(resp)

    resp = client.post(f"/api/v1/companies/{c.id}/restore")
    assert_status(resp, 200)
    assert resp.json()["id"] == c.id
