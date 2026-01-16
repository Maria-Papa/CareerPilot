from typing import Callable

from app.enums import FileType
from app.models.file import File
from app.models.user import User
from fastapi.testclient import TestClient
from tests.utils.api_assertions import assert_404, assert_list, assert_status


def test_create_file(client: TestClient, user_factory: Callable[..., User]):
    user = user_factory()
    payload = {
        "user_id": user.id,
        "file_url": "http://example.com/cv.pdf",
        "file_type": FileType.CV,
    }

    response = client.post("/api/v1/files", json=payload)
    assert_status(response, 201)
    data = response.json()
    assert data["file_url"] == payload["file_url"]


def test_get_file(
    client: TestClient,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
):
    user = user_factory()
    file = file_factory(user_id=user.id)

    response = client.get(f"/api/v1/files/{file.id}")
    assert_status(response, 200)
    assert response.json()["id"] == file.id


def test_get_file_not_found(client: TestClient):
    response = client.get("/api/v1/files/999999")
    assert_404(response)


def test_list_files(
    client: TestClient,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
):
    user = user_factory()
    file_factory(user_id=user.id)
    file_factory(user_id=user.id)

    response = client.get("/api/v1/files")
    assert_status(response, 200)
    assert_list(response)


def test_update_file(
    client: TestClient,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
):
    user = user_factory()
    file = file_factory(user_id=user.id)

    response = client.patch(
        f"/api/v1/files/{file.id}",
        json={"file_url": "http://updated.com"},
    )
    assert_status(response, 200)
    assert response.json()["file_url"] == "http://updated.com"


def test_delete_file(
    client: TestClient,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
):
    user = user_factory()
    file = file_factory(user_id=user.id)

    response = client.delete(f"/api/v1/files/{file.id}")
    assert_status(response, 204)


def test_restore_file(
    client: TestClient,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
):
    user = user_factory()
    file = file_factory(user_id=user.id)

    client.delete(f"/api/v1/files/{file.id}")
    response = client.post(f"/api/v1/files/{file.id}/restore")
    assert_status(response, 200)
    assert response.json()["deleted_at"] is None
