from typing import Callable

import pytest
from app.models.company import Company
from app.models.job import Job
from app.models.tag import Tag
from app.models.user import User
from fastapi.testclient import TestClient
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_job_tag(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    tag_factory: Callable[..., Tag],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)
    tag = tag_factory()

    resp = client.post(f"/api/v1/jobs/{job.id}/tags", json={"tag_id": tag.id})
    assert_status(resp, 201)

    resp = client.get(f"/api/v1/jobs/{job.id}/tags")
    assert_status(resp, 200)
    assert any(t["tag_id"] == tag.id for t in resp.json())


def test_update_job_tag(
    client: TestClient,
    user_factory,
    company_factory,
    job_factory,
    tag_factory,
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)
    tag1 = tag_factory()
    tag2 = tag_factory()

    client.post(f"/api/v1/jobs/{job.id}/tags", json={"tag_id": tag1.id})

    resp = client.patch(
        f"/api/v1/jobs/{job.id}/tags/{tag1.id}",
        json={"tag_id": tag2.id},
    )
    assert_status(resp, 200)
    assert resp.json()["tag_id"] == tag2.id


def test_delete_job_tag(
    client: TestClient,
    user_factory,
    company_factory,
    job_factory,
    tag_factory,
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)
    tag = tag_factory()

    client.post(f"/api/v1/jobs/{job.id}/tags", json={"tag_id": tag.id})

    resp = client.delete(f"/api/v1/jobs/{job.id}/tags/{tag.id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}/tags")
    assert all(t["tag_id"] != tag.id for t in resp.json())
