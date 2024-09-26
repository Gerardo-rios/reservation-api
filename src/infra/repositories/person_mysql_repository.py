from typing import Optional

from src.domain import entities, interfaces
from src.infra import db_models


class PersonMySQLRepository(interfaces.PersonRepositoryInterface):
    def __init__(self) -> None:
        self.__session = db_models.db_base.Session

    def __db_person_to_entity_person(
        self, db_person: db_models.PersonDBModel
    ) -> entities.Person:
        return entities.Person(
            person_id=db_person.person_id,
            name=db_person.name,
            phone=db_person.phone,
            address=db_person.address,
            city=db_person.city,
            country=db_person.country,
        )

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
        db_person = (
            self.__session.query(db_models.PersonDBModel).filter_by(phone=phone).first()
        )
        if db_person is None:
            return None
        return self.__db_person_to_entity_person(db_person)
