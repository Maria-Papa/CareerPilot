from typing import Sequence

from app.core import EntityNotFoundError
from app.models import CostOfLiving
from app.repositories.cost_of_living import CostOfLivingRepository
from app.repositories.location import LocationRepository
from app.schemas.cost_of_living import CostOfLivingCreate, CostOfLivingUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class CostOfLivingService(BaseService[CostOfLiving]):
    def __init__(self, repository=None, location_repo=None):
        repository = repository or CostOfLivingRepository()
        self.location_repo = location_repo or LocationRepository()
        super().__init__(repository)

    def _ensure_location_exists(self, session: Session, location_id: int):
        if self.location_repo.find_one(session, id=location_id) is None:
            raise EntityNotFoundError("Location not found")

    def list_costs(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[CostOfLiving]:
        return self.list(session, offset=offset, limit=limit)

    def get_cost(self, session: Session, col_id: int) -> CostOfLiving:
        col = self.get(session, col_id)
        if col is None:
            raise EntityNotFoundError("Cost of living entry not found")
        return col

    def create_cost(self, session: Session, data: CostOfLivingCreate) -> CostOfLiving:
        self._ensure_location_exists(session, data.location_id)
        col = CostOfLiving(**data.model_dump())
        return self.create(session, col)

    def update_cost(
        self, session: Session, col: CostOfLiving, data: CostOfLivingUpdate
    ) -> CostOfLiving:
        if data.location_id is not None:
            self._ensure_location_exists(session, data.location_id)

        values = data.model_dump(exclude_unset=True)
        return self.update(session, col, values)

    def adjust_yearly_cost(
        self, session: Session, col: CostOfLiving, new_cost: int
    ) -> CostOfLiving:
        return self.update(session, col, {"yearly_cost": new_cost})
