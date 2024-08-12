import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import UUID
from . import DbBase


class RolDBModel(DbBase):
    __tablename__ = "roles"

    rol_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, role_name: str, description: str) -> None:
        self.rol_id = uuid.uuid4()
        self.role_name = role_name
        self.description = description
