from typing import Callable

import pytest
from app.models.company import Company
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_restore_nonexistent_company(client: TestClient) -> None:
    resp = client.post("/api/v1/companies/999999/restore")
    assert resp.status_code == 404


def test_delete_nonexistent_company(client: TestClient) -> None:
    resp = client.delete("/api/v1/companies/999999")
    assert resp.status_code == 404


def test_restore_non_deleted_company(
    client: TestClient,
    company_factory: Callable[..., Company],
) -> None:
    c = company_factory(name="EdgeCase")
    resp = client.post(f"/api/v1/companies/{c.id}/restore")
    assert resp.status_code == 200
    assert resp.json()["id"] == c.id


def test_delete_twice_returns_404(
    client: TestClient,
    company_factory: Callable[..., Company],
) -> None:
    c = company_factory(name="EdgeCase")
    resp = client.delete(f"/api/v1/companies/{c.id}")
    assert resp.status_code == 204

    resp = client.delete(f"/api/v1/companies/{c.id}")
    assert resp.status_code == 404
