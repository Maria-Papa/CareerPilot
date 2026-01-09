from app.models import User
from app.repositories import SoftDeleteBaseRepository


class UserRepository(SoftDeleteBaseRepository[User]):
    def __init__(self):
        super().__init__(User)
