from app.models.user import User
from app.repositories.soft_delete_base import SoftDeleteBaseRepository


class UserRepository(SoftDeleteBaseRepository[User]):
    def __init__(self):
        super().__init__(User)
