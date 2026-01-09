from app.models import Company
from app.repositories import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)
