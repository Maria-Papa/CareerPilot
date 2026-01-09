from app.models import Currency
from app.repositories import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(Currency)
