import pytest
from app.enums.job_event_type import JobEventType
from app.models.job_event import JobEvent
from app.repositories.job_event import JobEventRepository
from sqlalchemy.orm import Session
from tests.factories.company import create_company
from tests.factories.job import create_job
from tests.factories.job_event import create_job_event
from tests.factories.user import create_user

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> JobEventRepository:
    return JobEventRepository()


def test_add_and_get_job_event(repo: JobEventRepository, db_session: Session) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    event = JobEvent(job_id=job.id, event_type=JobEventType.APPLICATION_SUBMITTED)
    created = repo.add(db_session, event)

    fetched = repo.get(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_all_job_events(repo: JobEventRepository, db_session: Session) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    create_job_event(db_session, job_id=job.id)
    create_job_event(db_session, job_id=job.id)

    events = repo.get_all(db_session)
    assert len(events) == 2


def test_update_job_event(repo: JobEventRepository, db_session: Session) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    event = create_job_event(db_session, job_id=job.id)
    updated = repo.update(db_session, event, {"payload": {"x": 1}})

    assert updated.payload == {"x": 1}


def test_delete_job_event(repo: JobEventRepository, db_session: Session) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)

    event = create_job_event(db_session, job_id=job.id)
    repo.delete(db_session, event)

    assert repo.get(db_session, event.id) is None
