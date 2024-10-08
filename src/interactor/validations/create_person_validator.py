from typing import Dict

from src.interactor import errors

from . import BaseInputValidator


class CreatePersonInputDtoValidator(BaseInputValidator):
    def __init__(self, data: Dict[str, str]) -> None:
        super().__init__(data)
        self.data = data
        self.__schema = {
            "name": {
                "type": "string",
                "minlength": 2,
                "maxlength": 255,
                "required": True,
                "empty": False,
            },
            "phone": {
                "type": "string",
                "minlength": 10,
                "maxlength": 10,
                "required": True,
                "empty": False,
            },
            "address": {
                "type": "string",
                "minlength": 8,
                "maxlength": 255,
                "required": True,
                "empty": False,
            },
            "city": {
                "type": "string",
                "minlength": 4,
                "maxlength": 255,
                "required": True,
                "empty": False,
            },
            "country": {
                "type": "string",
                "minlength": 2,
                "maxlength": 50,
                "required": True,
                "empty": False,
            },
        }

    def validate(self) -> None:
        super().verify(self.__schema)
        self.__validate_country()
        self.__validate_city()

    def __validate_country(self) -> None:
        if self.data["country"].lower() != "ecuador":
            raise errors.FieldValueNotPermittedException(
                "Country", self.data["country"]
            )

    def __validate_city(self) -> None:
        if self.data["city"].lower() != "loja":
            raise errors.FieldValueNotPermittedException("City", self.data["city"])
