from typing import Any, Callable

import pytest
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.api


def test_create_user(client: TestClient, db_session: Session) -> None:
    payload: dict[str, Any] = {
        "email": "user@example.com",
        "password": "pwd",
        "is_active": True,
        "is_verified": False,
    }

    response = client.post("/api/v1/users", json=payload)
    assert_status(response, 201)
    data = response.json()
    assert data["email"] == payload["email"]


def test_get_user(client: TestClient, user_factory: Callable[..., User]) -> None:
    user: User = user_factory()
    response = client.get(f"/api/v1/users/{user.id}")
    assert_status(response, 200)
    assert response.json()["id"] == user.id


def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/users/999999")
    assert_404(response)


def test_list_users(client: TestClient, user_factory: Callable[..., User]) -> None:
    user_factory()
    user_factory()
    response = client.get("/api/v1/users")
    assert_status(response, 200)
    assert_list(response)


def test_update_user(client: TestClient, user_factory: Callable[..., User]) -> None:
    user: User = user_factory()
    response = client.patch(
        f"/api/v1/users/{user.id}",
        json={"is_verified": True},
    )
    assert_status(response, 200)
    assert response.json()["is_verified"] is True


def test_delete_user(client: TestClient, user_factory: Callable[..., User]) -> None:
    user: User = user_factory()
    response = client.delete(f"/api/v1/users/{user.id}")
    assert_status(response, 204)


def test_restore_user(client: TestClient, user_factory: Callable[..., User]) -> None:
    user: User = user_factory()
    client.delete(f"/api/v1/users/{user.id}")
    response = client.post(f"/api/v1/users/{user.id}/restore")
    assert_status(response, 200)
    assert response.json()["deleted_at"] is None
