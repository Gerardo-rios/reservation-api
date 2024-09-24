from typing import Optional

from src.domain import entities, interfaces
from src.infra import db_models


class PersonMySQLRepository(interfaces.PersonRepositoryInterface):
    def __init__(self) -> None:
        self.__session = db_models.db_base.Session

    def create(
        self,
        name: str,
        phone: str,
        address: str,
        city: str,
        country: str,
    ) -> Optional[str]:
        pass

    def get_by_phone(self, phone: str) -> Optional[entities.Person]:
        pass
