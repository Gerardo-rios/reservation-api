import uuid
from typing import Optional

from src.domain import Account, Person, Role
from src.domain import Session as SessionDomain
from src.infra import AccountDBModel, PersonDBModel, RolDBModel, Session
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginRepositoryInterface


class LoginMySQLRepository(LoginRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(
        self,
        db_row_account: AccountDBModel,
        db_row_person: PersonDBModel,
        db_row_role: RolDBModel,
    ) -> Optional[SessionDomain]:
        return SessionDomain(
            account=Account(
                account_id=db_row_account.account_id,
                email=db_row_account.email,
                password=db_row_account.password,
                user=db_row_account.username,
                photo=db_row_account.photo,
                status=db_row_account.status,
            ),
            person=Person(
                person_id=db_row_person.person_id,
                name=db_row_person.name,
                phone=db_row_person.phone,
                address=db_row_person.address,
                city=db_row_person.city,
                country=db_row_person.country,
            ),
            role=Role(
                role_id=db_row_role.role_id,
                role_name=db_row_role.role_name,
                description=db_row_role.description,
            ),
        )

    def login(self, email: str, password: str) -> Optional[SessionDomain]:
        account = self.__session.query(AccountDBModel).filter_by(email=email).first()
        if account is None or account.password != password:
            return None
        if not account.status:
            raise AuthenticationError("Account is inactive")
        person = (
            self.__session.query(PersonDBModel)
            .filter_by(person_id=account.person_id)
            .first()
        )
        role = (
            self.__session.query(RolDBModel).filter_by(role_id=account.role_id).first()
        )
        return self.__db_to_entity(account, person, role)
