import pytest
from app.repositories.job_file_attachment import JobFileAttachmentRepository
from sqlalchemy.orm import Session
from tests.factories.company import create_company
from tests.factories.file import create_file
from tests.factories.job import create_job
from tests.factories.job_file_attachment import create_job_file_attachment
from tests.factories.user import create_user

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> JobFileAttachmentRepository:
    return JobFileAttachmentRepository()


def test_add_and_get_job_file_attachment(
    repo: JobFileAttachmentRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    file = create_file(db_session, user_id=user.id)

    attachment = create_job_file_attachment(
        db_session,
        job_id=job.id,
        file_id=file.id,
    )

    fetched = repo.get(db_session, attachment.id)
    assert fetched is not None
    assert fetched.id == attachment.id


def test_get_all_and_find_job_file_attachment(
    repo: JobFileAttachmentRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    file = create_file(db_session, user_id=user.id)

    a1 = create_job_file_attachment(db_session, job_id=job.id, file_id=file.id)
    a2 = create_job_file_attachment(db_session, job_id=job.id, file_id=file.id)

    all_attachments = repo.get_all(db_session)
    assert any(a.id == a1.id for a in all_attachments)
    assert any(a.id == a2.id for a in all_attachments)

    found = repo.find(db_session, job_id=job.id)
    assert any(a.job_id == job.id for a in found)


def test_update_job_file_attachment(
    repo: JobFileAttachmentRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    file = create_file(db_session, user_id=user.id)

    attachment = create_job_file_attachment(
        db_session,
        job_id=job.id,
        file_id=file.id,
    )

    updated = repo.update(db_session, attachment, {"is_active": False})
    assert updated.is_active is False


def test_soft_delete_and_restore_job_file_attachment(
    repo: JobFileAttachmentRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    file = create_file(db_session, user_id=user.id)

    attachment = create_job_file_attachment(
        db_session,
        job_id=job.id,
        file_id=file.id,
    )

    repo.soft_delete(db_session, attachment)
    assert repo.get(db_session, attachment.id) is None

    incl = repo.get_including_deleted(db_session, attachment.id)
    assert incl is not None
    assert incl.deleted_at is not None

    repo.restore(db_session, incl)
    assert repo.get(db_session, attachment.id) is not None


def test_delete_permanent_job_file_attachment(
    repo: JobFileAttachmentRepository, db_session: Session
) -> None:
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    file = create_file(db_session, user_id=user.id)

    attachment = create_job_file_attachment(
        db_session,
        job_id=job.id,
        file_id=file.id,
    )

    repo.delete(db_session, attachment)
    assert repo.get_including_deleted(db_session, attachment.id) is None
