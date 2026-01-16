from typing import Callable

import pytest
from app.enums.job_status import JobStatus
from app.models.company import Company
from app.models.job import Job
from app.models.location import Location
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_job(
    client: TestClient,
    db_session: Session,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    payload = {
        "user_id": user.id,
        "company_id": company.id,
        "location_id": location.id,
        "title": "API Job",
        "current_status": JobStatus.APPLIED,
    }

    resp = client.post("/api/v1/jobs", json=payload)
    assert_status(resp, 201)

    job_id = resp.json()["id"]

    resp = client.get(f"/api/v1/jobs/{job_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == job_id


def test_list_jobs(
    client: TestClient,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    job_factory(user_id=user.id, company_id=company.id, location_id=location.id)
    job_factory(user_id=user.id, company_id=company.id, location_id=location.id)

    resp = client.get("/api/v1/jobs")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_job(
    client: TestClient,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    job = job_factory(user_id=user.id, company_id=company.id, location_id=location.id)

    resp = client.patch(f"/api/v1/jobs/{job.id}", json={"title": "Updated"})
    assert_status(resp, 200)
    assert resp.json()["title"] == "Updated"


def test_delete_and_restore_job(
    client: TestClient,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    job = job_factory(user_id=user.id, company_id=company.id, location_id=location.id)

    resp = client.delete(f"/api/v1/jobs/{job.id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}")
    assert_404(resp)

    resp = client.post(f"/api/v1/jobs/{job.id}/restore")
    assert_status(resp, 200)
    assert resp.json()["id"] == job.id


def test_change_status(
    client: TestClient,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    job = job_factory(user_id=user.id, company_id=company.id, location_id=location.id)

    resp = client.post(f"/api/v1/jobs/{job.id}/status/{JobStatus.INTERVIEW}")
    assert_status(resp, 200)
    assert resp.json()["current_status"] == JobStatus.INTERVIEW


def test_attach_file(
    client: TestClient,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    location_factory: Callable[..., Location],
) -> None:
    user = user_factory()
    company = company_factory()
    location = location_factory()

    job = job_factory(user_id=user.id, company_id=company.id, location_id=location.id)

    resp = client.post(f"/api/v1/jobs/{job.id}/attachments?file_id=1&version=1")
    assert_status(resp, 201)
