import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import UUID
from . import DbBase, RolDBModel, PersonDBModel


class AccountDBModel(DbBase):
    __tablename__ = "accounts"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(binary=False), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    rol_id: Mapped[uuid.UUID] = mapped_column(
        UUID(binary=False), ForeignKey("roles.rol_id"), nullable=False, unique=True
    )
    rol = relationship(RolDBModel)
    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(binary=False), ForeignKey("persons.person_id"), nullable=False, unique=True
    )
    person = relationship(PersonDBModel)

    def __init__(
        self,
        email: str,
        password: str,
        username: str,
        photo: str,
        status: bool,
        rol_id: uuid.UUID,
        person_id: uuid.UUID,
    ) -> None:
        self.account_id = uuid.uuid4()
        self.email = email
        self.password = password
        self.username = username
        self.photo = photo
        self.status = status
        self.rol_id = rol_id
        self.person_id = person_id
