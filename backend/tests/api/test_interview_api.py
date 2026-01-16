from datetime import datetime, timezone
from typing import Callable

import pytest
from app.enums.interview_type import InterviewType
from app.models.company import Company
from app.models.interview import Interview
from app.models.job import Job
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_interview(
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
        "interview_type": InterviewType.HR_SCREEN,
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "outcome": None,
        "notes": "First call",
    }

    resp = client.post(f"/api/v1/jobs/{job.id}/interviews", json=payload)
    assert_status(resp, 201)

    interview_id = resp.json()["id"]

    resp = client.get(f"/api/v1/jobs/{job.id}/interviews/{interview_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == interview_id


def test_list_interviews(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    interview_factory: Callable[..., Interview],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview_factory(job_id=job.id)
    interview_factory(job_id=job.id)

    resp = client.get(f"/api/v1/jobs/{job.id}/interviews")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_interview(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    interview_factory: Callable[..., Interview],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id, notes="Old")

    resp = client.patch(
        f"/api/v1/jobs/{job.id}/interviews/{interview.id}",
        json={"notes": "New"},
    )
    assert_status(resp, 200)
    assert resp.json()["notes"] == "New"


def test_delete_interview(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    interview_factory: Callable[..., Interview],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id)

    resp = client.delete(f"/api/v1/jobs/{job.id}/interviews/{interview.id}")
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}/interviews/{interview.id}")
    assert_404(resp)


def test_reschedule_interview(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    interview_factory: Callable[..., Interview],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id)

    new_time = datetime.now(timezone.utc).isoformat()
    resp = client.post(
        f"/api/v1/jobs/{job.id}/interviews/{interview.id}/reschedule",
        params={"scheduled_at": new_time},
    )
    assert_status(resp, 200)
    assert resp.json()["scheduled_at"].startswith(new_time[:19])
