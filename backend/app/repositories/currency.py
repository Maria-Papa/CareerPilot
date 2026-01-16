from app.models.currency import Currency
from app.repositories.base import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self) -> None:
        super().__init__(Currency)
