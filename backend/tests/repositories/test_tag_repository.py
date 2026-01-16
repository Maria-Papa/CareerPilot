from app.models.tag import Tag
from app.repositories.tag import TagRepository
from sqlalchemy.orm import Session
from tests.factories.tag import create_tag


def test_add_and_get_tag(db_session: Session) -> None:
    repo = TagRepository()
    tag = Tag(name="backend")
    created = repo.add(db_session, tag)

    fetched = repo.get(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "backend"


def test_get_all_tags(db_session: Session) -> None:
    repo = TagRepository()
    create_tag(db_session, name="t1")
    create_tag(db_session, name="t2")

    tags = repo.get_all(db_session)
    assert len(tags) == 2


def test_update_tag(db_session: Session) -> None:
    repo = TagRepository()
    tag = create_tag(db_session, name="old")

    updated = repo.update(db_session, tag, {"name": "new"})
    assert updated.name == "new"


def test_delete_tag(db_session: Session) -> None:
    repo = TagRepository()
    tag = create_tag(db_session, name="to-delete")

    repo.delete(db_session, tag)
    assert repo.get(db_session, tag.id) is None
