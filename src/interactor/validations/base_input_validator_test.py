from typing import Any, Dict
import pytest
from . import BaseInputValidator


class BaseValidator(BaseInputValidator):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.schema = {
            "name": {"type": "string", "required": True},
            "age": {"type": "integer", "required": True},
        }

    def validate(self) -> None:
        super().verify(self.schema)


def test_base_validator_with_valid_data() -> None:
    data = {"name": "John Doe", "age": 30}
    validator = BaseValidator(data)
    validator.validate()


def test_base_validator_with_invalid_data() -> None:
    data = {"name": "John Doe", "age": "30"}
    validator = BaseValidator(data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert str(e.value) == "age: must be of integer type"


def test_base_validator_with_missing_data() -> None:
    data = {"name": "John Doe"}
    validator = BaseValidator(data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert str(e.value) == "age: required field"


def test_base_validator_with_empty_data() -> None:
    data: Dict[str, Any] = {}
    validator = BaseValidator(data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert str(e.value) == "age: required field\nname: required field"
