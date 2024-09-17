from typing import Optional

import bcrypt

from src.domain import Account
from src.domain.interfaces import LoginRepositoryInterface
from src.infra import AccountDBModel, Session
from src.interactor.errors import AuthenticationError


class LoginMySQLRepository(LoginRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(
        self,
        db_row_account: AccountDBModel,
    ) -> Optional[Account]:
        return Account(
            account_id=db_row_account.account_id,
            email=db_row_account.email,
            password=db_row_account.password,
            user=db_row_account.username,
            photo=db_row_account.photo,
            status=db_row_account.status,
        )

    def login(self, email: str, password: str) -> Optional[Account]:
        account = self.__session.query(AccountDBModel).filter_by(email=email).first()
        if account is None:
            return None
        password_matches = bcrypt.checkpw(
            password.encode("utf-8"), account.password.encode("utf-8")
        )
        if not password_matches:
            return None
        if not account.status:
            raise AuthenticationError("Account is inactive")
        return self.__db_to_entity(account)
