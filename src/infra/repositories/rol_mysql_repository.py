from typing import Optional

from src.domain import Role
from src.infra import RolDBModel, Session
from src.interactor.interfaces import RoleRepositoryInterface


class RolMySQLRepository(RoleRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(self, db_row: RolDBModel) -> Optional[Role]:
        return Role(
            role_id=db_row.role_id,
            role_name=db_row.role_name,
            description=db_row.description,
        )

    def get(self, role_name: str) -> Optional[Role]:
        db_row = self.__session.query(RolDBModel).filter_by(role_name=role_name).first()
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)
