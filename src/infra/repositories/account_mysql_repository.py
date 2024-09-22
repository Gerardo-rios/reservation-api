import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.domain import entities, interfaces
from src.infra import db_models
from src.interactor import errors


class AccountMySQLRepository(interfaces.AccountRepositoryInterface):
    def __init__(self) -> None:
        self.__session = db_models.db_base.Session

    def __db_to_entity(
        self, db_row: db_models.AccountDBModel
    ) -> Optional[entities.Account]:
        return entities.Account(
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
        person_id: str,
    ) -> Optional[entities.Account]:
        new_account = db_models.AccountDBModel(
            account_id=uuid.uuid4(),
            email=email,
            password=password,
            username=user,
            photo=photo,
            status=status,
            role_id=role_id,
            person_id=person_id,
        )

        try:
            self.__session.add(new_account)
            self.__session.commit()
            self.__session.refresh(new_account)
        except IntegrityError as e:
            self.__session.rollback()
            if "phone" in str(e.orig):
                raise errors.UniqueViolationError("Phone number already exists")
            raise errors.UniqueViolationError("Account email already exists")

        if new_account is not None:
            return self.__db_to_entity(new_account)
        return None

    def get(self, account_id: str) -> Optional[entities.Account]:
        db_row = (
            self.__session.query(db_models.AccountDBModel)
            .filter_by(account_id=account_id)
            .first()
        )
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)

    def update(self, account: entities.Account) -> Optional[entities.Account]:
        account_db_model = db_models.AccountDBModel(
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
            self.__session.query(db_models.AccountDBModel)
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
