import pytest
from app.enums.job_status import JobStatus
from app.repositories.job_status_history import JobStatusHistoryRepository
from sqlalchemy.orm import Session
from tests.factories.company import create_company
from tests.factories.job import create_job
from tests.factories.job_status_history import create_job_status_history
from tests.factories.user import create_user

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> JobStatusHistoryRepository:
    return JobStatusHistoryRepository()


def test_add_and_get_job_status_history(
    repo: JobStatusHistoryRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    history = create_job_status_history(db_session, job_id=job.id)

    fetched = repo.get(db_session, history.id)
    assert fetched is not None
    assert fetched.id == history.id


def test_get_all_and_find_job_status_history(
    repo: JobStatusHistoryRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    h1 = create_job_status_history(db_session, job_id=job.id, status=JobStatus.APPLIED)
    h2 = create_job_status_history(
        db_session, job_id=job.id, status=JobStatus.INTERVIEW
    )

    all_history = repo.get_all(db_session)
    assert any(h.id == h1.id for h in all_history)
    assert any(h.id == h2.id for h in all_history)

    found = repo.find(db_session, job_id=job.id)
    assert all(h.job_id == job.id for h in found)


def test_update_job_status_history(
    repo: JobStatusHistoryRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    history = create_job_status_history(db_session, job_id=job.id)

    updated = repo.update(db_session, history, {"status": JobStatus.INTERVIEW})
    assert updated.status == JobStatus.INTERVIEW


def test_delete_job_status_history(
    repo: JobStatusHistoryRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    history = create_job_status_history(db_session, job_id=job.id)

    repo.delete(db_session, history)
    assert repo.get(db_session, history.id) is None
