from sqlalchemy.orm import Session
from app.models import User
from app.repositories import UserRepository
from app.services import BaseService
from app.schemas import UserCreate, UserUpdate


class UserService(BaseService[User]):
    repository: UserRepository

    def __init__(self):
        super().__init__(UserRepository())

    def create_user(self, session: Session, data: UserCreate) -> User:
        user = User(**data.model_dump())
        return self.create(session, user)

    def update_user(self, session: Session, user: User, data: UserUpdate) -> User:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, user, values)
