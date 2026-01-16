import uuid

from app.models.tag import Tag
from sqlalchemy.orm import Session


def create_tag(db_session: Session, **kwargs) -> Tag:
    defaults = {
        "name": f"tag-{uuid.uuid4().hex[:8]}",
    }

    defaults.update(kwargs)

    tag = Tag(**defaults)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag
