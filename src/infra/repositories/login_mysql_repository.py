from typing import Optional

import bcrypt

from src.domain import entities, interfaces
from src.infra import db_models
from src.interactor import errors


class LoginMySQLRepository(interfaces.LoginRepositoryInterface):
    def __init__(self) -> None:
        self.__session = db_models.db_base.Session

    def __db_to_entity(
        self,
        db_row_account: db_models.AccountDBModel,
    ) -> Optional[entities.Account]:
        return entities.Account(
            account_id=db_row_account.account_id,
            email=db_row_account.email,
            password=db_row_account.password,
            user=db_row_account.username,
            photo=db_row_account.photo,
            status=db_row_account.status,
        )

    def login(self, email: str, password: str) -> Optional[entities.Account]:
        account = (
            self.__session.query(db_models.AccountDBModel)
            .filter_by(email=email)
            .first()
        )
        if account is None:
            return None
        password_matches = bcrypt.checkpw(
            password.encode("utf-8"), account.password.encode("utf-8")
        )
        if not password_matches:
            return None
        if not account.status:
            raise errors.AuthenticationError("Account is inactive")
        return self.__db_to_entity(account)
