from datetime import datetime, timezone
from typing import Callable

import pytest
from app.enums.job_status import JobStatus
from app.models.company import Company
from app.models.job import Job
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_job_status_history(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
):
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    payload = {
        "status": JobStatus.APPLIED.value,
    }

    resp = client.post(f"/api/v1/jobs/{job.id}/status-history", json=payload)
    assert_status(resp, 201)

    history_id = resp.json()["id"]

    resp = client.get(f"/api/v1/jobs/{job.id}/status-history/{history_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == history_id
    assert resp.json()["job_id"] == job.id


def test_list_job_status_history(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
):
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    payload1 = {"status": JobStatus.APPLIED.value}
    payload2 = {"status": JobStatus.INTERVIEW.value}

    client.post(f"/api/v1/jobs/{job.id}/status-history", json=payload1)
    client.post(f"/api/v1/jobs/{job.id}/status-history", json=payload2)

    resp = client.get(f"/api/v1/jobs/{job.id}/status-history")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_job_status_history(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
):
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    payload = {"status": JobStatus.APPLIED.value}
    resp = client.post(f"/api/v1/jobs/{job.id}/status-history", json=payload)
    assert_status(resp, 201)
    history_id = resp.json()["id"]

    resp = client.patch(
        f"/api/v1/jobs/{job.id}/status-history/{history_id}",
        json={"status": JobStatus.INTERVIEW.value},
    )
    assert_status(resp, 200)
    assert resp.json()["status"] == JobStatus.INTERVIEW.value


def test_delete_job_status_history(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
):
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    payload = {"status": JobStatus.APPLIED.value}
    resp = client.post(f"/api/v1/jobs/{job.id}/status-history", json=payload)
    assert_status(resp, 201)
    history_id = resp.json()["id"]

    resp = client.delete(f"/api/v1/jobs/{job.id}/status-history/{history_id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}/status-history/{history_id}")
    assert_404(resp)
