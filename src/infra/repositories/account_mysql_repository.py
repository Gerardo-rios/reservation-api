import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.domain import Account, Person
from src.infra import AccountDBModel, PersonDBModel, Session
from src.interactor import AccountRepositoryInterface, UniqueViolationError


class AccountMySQLRepository(AccountRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(self, db_row: AccountDBModel) -> Optional[Account]:
        return Account(
            account_id=db_row.account_id,
            email=db_row.email,
            password=db_row.password,
            user=db_row.username,
            photo=db_row.photo,
            status=db_row.status,
        )

    def create(
        self,
        email: str,
        password: str,
        user: str,
        photo: str,
        status: bool,
        role_id: str,
        person: Person,
    ) -> Optional[Account]:
        new_person = PersonDBModel(
            person_id=person.person_id,
            name=person.name,
            phone=person.phone,
            address=person.address,
            city=person.city,
            country=person.country,
        )

        new_account = AccountDBModel(
            account_id=uuid.uuid4(),
            email=email,
            password=password,
            username=user,
            photo=photo,
            status=status,
            role_id=role_id,
            person_id=new_person.person_id,
        )

        try:
            self.__session.add(new_person)
            self.__session.add(new_account)
            self.__session.commit()
            self.__session.refresh(new_account)
        except IntegrityError as e:
            self.__session.rollback()
            if "phone" in str(e.orig):
                raise UniqueViolationError("Phone number already exists")
            raise UniqueViolationError("Account email already exists")

        if new_account is not None:
            return self.__db_to_entity(new_account)
        return None

    def get(self, account_id: str) -> Optional[Account]:
        db_row = (
            self.__session.query(AccountDBModel)
            .filter_by(account_id=account_id)
            .first()
        )
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)

    def update(self, account: Account) -> Optional[Account]:
        account_db_model = AccountDBModel(
            account_id=account.account_id,
            email=account.email,
            password=account.password,
            username=account.user,
            photo=account.photo,
            status=account.status,
            role_id="",
            person_id="",
        )
        result = (
            self.__session.query(AccountDBModel)
            .filter_by(account_id=account.account_id)
            .update(
                {
                    "password": account.password,
                    "photo": account.photo,
                    "status": account.status,
                }
            )
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(account_db_model)
