from app.models.tag import Tag
from sqlalchemy.orm import Session


def create_tag(session: Session, *, name: str = "tag-1") -> Tag:
    tag = Tag(name=name)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag
