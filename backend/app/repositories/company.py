from app.models import Company
from app.repositories.soft_delete_base import SoftDeleteBaseRepository


class CompanyRepository(SoftDeleteBaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)
