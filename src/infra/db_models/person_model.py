import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import DbBase


class PersonDBModel(DbBase):
    __tablename__ = "persons"

    person_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

    def __init__(
        self, name: str, phone: str, address: str, city: str, country: str
    ) -> None:
        self.person_id = str(uuid.uuid4())
        self.name = name
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
