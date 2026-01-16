from typing import Sequence

from app.core.errors import ConflictError, EntityNotFoundError
from app.models import User
from app.repositories.user import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.services.soft_delete_base import SoftDeleteService
from sqlalchemy.orm import Session


class UserService(SoftDeleteService[User]):
    def __init__(self, repository: UserRepository | None = None) -> None:
        repository = repository or UserRepository()
        super().__init__(repository)

    def list_users(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[User]:
        return self.list(session, offset=offset, limit=limit)

    def get_user(self, session: Session, user_id: int) -> User:
        user = self.repository.get(session, user_id)
        if user is None:
            raise EntityNotFoundError("User not found")
        return user

    def get_user_including_deleted(self, session: Session, user_id: int) -> User:
        user = self.soft_repo.get_including_deleted(session, user_id)
        if user is None:
            raise EntityNotFoundError("User not found")
        return user

    def create_user(self, session: Session, data: UserCreate) -> User:
        existing = self.repository.find_one(session, email=data.email)
        if existing is not None:
            raise ConflictError("Email already exists")

        # TODO: plug in real hashing; for now map password -> password_hash
        user = User(
            email=data.email,
            password_hash=data.password,
            is_active=data.is_active,
            is_verified=data.is_verified,
        )
        return self.create(session, user)

    def update_user(self, session: Session, user: User, data: UserUpdate) -> User:
        values = data.model_dump(exclude_unset=True)
        if "password" in values:
            values["password_hash"] = values.pop("password")
        return self.update(session, user, values)
