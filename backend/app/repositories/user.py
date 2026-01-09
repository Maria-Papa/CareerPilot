from app.models import User
from app.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
