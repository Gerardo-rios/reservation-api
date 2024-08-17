import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import DbBase


class AccountDBModel(DbBase):
    __tablename__ = "accounts"

    account_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("roles.role_id"), nullable=False
    )
    rol = relationship("RolDBModel")
    person_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("persons.person_id"), nullable=False
    )
    person = relationship("PersonDBModel")
