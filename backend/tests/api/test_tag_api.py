from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.factories.tag import create_tag
from tests.utils.api_assertions import assert_status


def test_create_and_get_tag(client: TestClient) -> None:
    payload = {"name": "api-tag"}

    resp = client.post("/api/v1/tags", json=payload)
    assert_status(resp, 201)

    data = resp.json()
    tag_id = data["id"]
    assert data["name"] == "api-tag"

    resp_get = client.get(f"/api/v1/tags/{tag_id}")
    assert_status(resp_get, 200)
    data_get = resp_get.json()
    assert data_get["id"] == tag_id
    assert data_get["name"] == "api-tag"


def test_list_tags(
    client: TestClient,
    db_session: Session,
) -> None:
    create_tag(db_session, name="t1")
    create_tag(db_session, name="t2")

    resp = client.get("/api/v1/tags")
    assert_status(resp, 200)

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_update_tag(
    client: TestClient,
    db_session: Session,
) -> None:
    tag = create_tag(db_session, name="old")

    resp = client.patch(f"/api/v1/tags/{tag.id}", json={"name": "new"})
    assert_status(resp, 200)

    data = resp.json()
    assert data["id"] == tag.id
    assert data["name"] == "new"


def test_delete_tag(
    client: TestClient,
    db_session: Session,
) -> None:
    tag = create_tag(db_session, name="to-delete")

    resp = client.delete(f"/api/v1/tags/{tag.id}")
    assert_status(resp, 204)

    resp_get = client.get(f"/api/v1/tags/{tag.id}")
    assert_status(resp_get, 404)
