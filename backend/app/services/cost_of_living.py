from sqlalchemy.orm import Session
from app.models import CostOfLiving
from app.repositories import CostOfLivingRepository
from app.schemas import CostOfLivingCreate, CostOfLivingUpdate
from app.services import BaseService


class CostOfLivingService(BaseService[CostOfLiving]):
    repository: CostOfLivingRepository

    def __init__(self):
        super().__init__(CostOfLivingRepository())

    def create_cost_of_living(
        self, session: Session, data: CostOfLivingCreate
    ) -> CostOfLiving:
        col = CostOfLiving(**data.model_dump())
        return self.create(session, col)

    def update_cost_of_living(
        self, session: Session, col: CostOfLiving, data: CostOfLivingUpdate
    ) -> CostOfLiving:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, col, values)

    def adjust_yearly_cost(
        self, session: Session, col: CostOfLiving, new_cost: int
    ) -> CostOfLiving:
        col.yearly_cost = new_cost
        return self.update(session, col, {"yearly_cost": new_cost})
