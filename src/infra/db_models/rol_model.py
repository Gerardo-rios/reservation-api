import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import DbBase


class RolDBModel(DbBase):
    __tablename__ = "roles"

    role_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
