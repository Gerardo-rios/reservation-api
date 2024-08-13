from typing import Optional
import uuid
from sqlalchemy.exc import IntegrityError
from src.domain import Person
from src.interactor import PersonRepositoryInterface, UniqueViolationError
from src.infra import Session, PersonDBModel


class PersonMySQLRepository(PersonRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(self, db_row: PersonDBModel) -> Optional[Person]:
        return Person(
            person_id=db_row.person_id,
            name=db_row.name,
            phone=db_row.phone,
            address=db_row.address,
            city=db_row.city,
            country=db_row.country,
        )

    def create(
        self, name: str, phone: str, address: str, city: str, country: str
    ) -> Optional[Person]:
        new_person = PersonDBModel(
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
            raise UniqueViolationError("Person phone already exists")

        if new_person is not None:
            return self.__db_to_entity(new_person)
        return None

    def get(self, person_id: str) -> Optional[Person]:
        db_row = (
            self.__session.query(PersonDBModel).filter_by(person_id=person_id).first()
        )
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)

    def update(self, person: Person) -> Optional[Person]:
        person_db_model = PersonDBModel(
            person_id=person.person_id,
            name=person.name,
            phone=person.phone,
            address=person.address,
            city=person.city,
            country=person.country,
        )
        result = (
            self.__session.query(PersonDBModel)
            .filter_by(person_id=person.person_id)
            .update(
                {
                    "name": person.name,
                    "phone": person.phone,
                    "address": person.address,
                    "city": person.city,
                    "country": person.country,
                }
            )
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(person_db_model)
