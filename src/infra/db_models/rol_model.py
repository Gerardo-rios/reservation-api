import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import DbBase


class RolDBModel(DbBase):
    __tablename__ = "roles"

    rol_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, role_name: str, description: str) -> None:
        self.rol_id = str(uuid.uuid4())
        self.role_name = role_name
        self.description = description
