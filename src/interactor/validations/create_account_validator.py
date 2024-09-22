import re
from typing import Any, Dict

from src.interactor import errors

from .base_input_validator import BaseInputValidator


class CreateAccountInputDtoValidator(BaseInputValidator):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.data = data
        self.__schema = {
            "email": {
                "type": "string",
                "minlength": 10,
                "maxlength": 255,
                "required": True,
                "empty": False,
            },
            "password": {
                "type": "string",
                "minlength": 8,
                "maxlength": 72,
                "required": True,
                "empty": False,
            },
            "user": {
                "type": "string",
                "minlength": 8,
                "maxlength": 255,
                "required": True,
                "empty": False,
            },
            "photo": {"type": "string", "required": False, "empty": True},
            "role_id": {"type": "string", "required": True, "empty": False},
            "person_id": {"type": "string", "required": True, "empty": False},
        }

    def validate(self) -> None:
        super().verify(self.__schema)
        self.__validate_email()
        self.__validate_password()

    def __validate_email(self) -> None:
        email = self.data["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise errors.EmailFormatException(email)

    def __validate_password(self) -> None:
        password = self.data["password"]
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>])[A-Za-z\d!@#$%^&*(),.?\":{}|<>]{8,}$"  # noqa
        if not re.match(pattern, password):
            raise errors.PasswordFormatException(password)
