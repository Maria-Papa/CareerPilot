import pytest
from tests.utils.api_assertions import (
    assert_404,
    assert_list,
    assert_status,
)

pytestmark = pytest.mark.integration


def test_create_and_get_company(client, db_session):
    payload = {"name": "ApiCo", "website": "https://api.co", "industry": "API"}
    resp = client.post("/companies", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    company_id = data["id"]

    resp = client.get(f"/companies/{company_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == company_id


def test_list_companies_endpoint(client, db_session, company_factory):
    company_factory(name="ListAPI1")
    company_factory(name="ListAPI2")

    resp = client.get("/companies")
    assert_status(resp, 200)
    assert_list(resp)


def test_patch_company(client, db_session, company_factory):
    c = company_factory(name="PatchMe")
    payload = {"name": "Patched"}

    resp = client.patch(f"/companies/{c.id}", json=payload)
    assert_status(resp, 200)
    assert resp.json()["name"] == "Patched"

    db_session.refresh(c)
    assert c.name == "Patched"


def test_delete_and_restore_endpoints(client, db_session, company_factory):
    c = company_factory(name="DeleteAPI")

    resp = client.delete(f"/companies/{c.id}")
    assert_status(resp, 204)

    resp = client.get(f"/companies/{c.id}")
    assert_404(resp)

    resp = client.post(f"/companies/{c.id}/restore")
    assert_status(resp, 200)
    assert resp.json()["id"] == c.id
