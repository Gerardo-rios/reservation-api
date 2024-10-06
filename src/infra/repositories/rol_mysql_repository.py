from typing import Optional

from src.domain import entities, interfaces
from src.infra import db_models


class RolMySQLRepository(interfaces.RoleRepositoryInterface):
    def __init__(self) -> None:
        self.__session = db_models.db_base.Session

    def __db_to_entity(self, db_row: db_models.RolDBModel) -> Optional[entities.Role]:
        return entities.Role(
            role_id=db_row.role_id,
            role_name=db_row.role_name,
            description=db_row.description,
        )

    def get_by_name(self, role_name: str) -> Optional[entities.Role]:
        db_row = (
            self.__session.query(db_models.RolDBModel)
            .filter_by(role_name=role_name)
            .first()
        )
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)

    def get_by_id(self, role_id: str) -> Optional[entities.Role]:
        db_row = (
            self.__session.query(db_models.RolDBModel)
            .filter_by(role_id=role_id)
            .first()
        )
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)
