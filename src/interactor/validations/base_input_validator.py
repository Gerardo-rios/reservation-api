from typing import Any, Dict

from cerberus import Validator


class BaseInputValidator:
    def __init__(self, data: Dict[str, str]):
        self.data = data
        self.errors: Dict[str, Any] = {}

    def verify(self, schema: Dict[str, Any]) -> None:
        validator = Validator(schema)

        if not validator.validate(self.data):
            self.errors = validator.errors
            self.__raise_validation_error()

    def __raise_validation_error(self) -> None:
        error_messages = []
        for field, errors in self.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        raise ValueError("\n".join(error_messages))
