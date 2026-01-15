from app.models import CostOfLiving
from app.repositories.base import BaseRepository


class CostOfLivingRepository(BaseRepository[CostOfLiving]):
    def __init__(self):
        super().__init__(CostOfLiving)
