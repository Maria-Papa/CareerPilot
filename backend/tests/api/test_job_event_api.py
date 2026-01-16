from typing import Callable

import pytest
from app.enums.job_event_type import JobEventType
from app.models.company import Company
from app.models.job import Job
from app.models.job_event import JobEvent
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_job_event(
    client: TestClient,
    db_session: Session,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    payload = {
        "event_type": JobEventType.APPLICATION_SUBMITTED,
        "payload": {"x": 1},
    }

    resp = client.post(f"/api/v1/jobs/{job.id}/job-events", json=payload)
    assert_status(resp, 201)

    event_id = resp.json()["id"]

    resp = client.get(f"/api/v1/jobs/{job.id}/job-events/{event_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == event_id


def test_list_job_events(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    job_event_factory: Callable[..., JobEvent],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    job_event_factory(job_id=job.id)
    job_event_factory(job_id=job.id)

    resp = client.get(f"/api/v1/jobs/{job.id}/job-events")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_job_event(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    job_event_factory: Callable[..., JobEvent],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    event = job_event_factory(job_id=job.id, payload={"old": True})

    resp = client.patch(
        f"/api/v1/jobs/{job.id}/job-events/{event.id}",
        json={"payload": {"updated": True}},
    )
    assert_status(resp, 200)
    assert resp.json()["payload"] == {"updated": True}


def test_delete_job_event(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    job_event_factory: Callable[..., JobEvent],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    event = job_event_factory(job_id=job.id)

    resp = client.delete(f"/api/v1/jobs/{job.id}/job-events/{event.id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}/job-events/{event.id}")
    assert_404(resp)
