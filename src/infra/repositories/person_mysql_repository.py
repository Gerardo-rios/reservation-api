import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.domain import entities, interfaces
from src.infra import db_models
from src.interactor import errors


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
        new_person = db_models.PersonDBModel(
            person_id=uuid.uuid4(),
            name=name,
            phone=phone,
            address=address,
            city=city,
            country=country,
        )

        try:
            self.__session.add(new_person)
            self.__session.commit()
            self.__session.refresh(new_person)
        except IntegrityError:
            self.__session.rollback()
            raise errors.UniqueViolationError("Phone number already exists")

        if new_person is not None:
            return str(new_person.person_id)
        return None

    def get_by_phone(self, phone: str) -> Optional[entities.Person]:
        db_person = (
            self.__session.query(db_models.PersonDBModel).filter_by(phone=phone).first()
        )
        if db_person is None:
            return None
        return self.__db_person_to_entity_person(db_person)

    def get_by_id(self, person_id: str) -> Optional[entities.Person]:
        db_person = (
            self.__session.query(db_models.PersonDBModel)
            .filter_by(person_id=person_id)
            .first()
        )
        if db_person is None:
            return None
        return self.__db_person_to_entity_person(db_person)
