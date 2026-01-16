import uuid

from app.models.user import User
from sqlalchemy.orm import Session


def create_user(db_session: Session, **kwargs) -> User:
    user = User(
        email=kwargs.get("email", f"user-{uuid.uuid4()}@example.com"),
        password_hash=kwargs.get("password_hash", "hashed"),
        is_active=kwargs.get("is_active", True),
        is_verified=kwargs.get("is_verified", False),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
