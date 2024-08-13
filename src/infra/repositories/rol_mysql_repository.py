from typing import Optional
import uuid
from sqlalchemy.exc import IntegrityError
from src.domain import Rol
from src.interactor import RolRepositoryInterface, UniqueViolationError
from src.infra import Session, RolDBModel


class RolMySQLRepository(RolRepositoryInterface):
    def __init__(self) -> None:
        self.__session = Session

    def __db_to_entity(self, db_row: RolDBModel) -> Optional[Rol]:
        return Rol(
            rol_id=db_row.rol_id,
            rol_name=db_row.role_name,
            description=db_row.description,
        )

    def create(
        self, role_name: Optional[str] = None, description: Optional[str] = None
    ) -> Optional[Rol]:
        try:
            if role_name is None and description is None:
                default_roles = [
                    RolDBModel(
                        rol_id=uuid.uuid4(),
                        role_name="admin",
                        description="Administrator with business permissions",
                    ),
                    RolDBModel(
                        rol_id=uuid.uuid4(),
                        role_name="user",
                        description="User with user usage permissions",
                    ),
                ]
                self.__session.add_all(default_roles)
                self.__session.commit()
                return [self.__db_to_entity(role) for role in default_roles]  # type: ignore  # noqa
            else:
                new_role = RolDBModel(
                    rol_id=uuid.uuid4(), role_name=role_name, description=description
                )
                self.__session.add(new_role)
                self.__session.commit()
                self.__session.refresh(new_role)
                return self.__db_to_entity(new_role)
        except IntegrityError:
            self.__session.rollback()
            raise UniqueViolationError("Role name already exists")

    def get(self, role_name: str) -> Optional[Rol]:
        db_row = self.__session.query(RolDBModel).filter_by(role_name=role_name).first()
        if db_row is None:
            return None
        return self.__db_to_entity(db_row)
