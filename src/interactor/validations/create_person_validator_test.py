from typing import Dict

import pytest
from pytest_mock import MockFixture

from src.interactor.errors import FieldValueNotPermittedException

from . import CreatePersonInputDtoValidator


@pytest.fixture
def test_data(fixture_person_data: Dict[str, str]) -> Dict[str, str]:
    return fixture_person_data


def test_create_person_input_dto_validator(
    test_data: Dict[str, str], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    schema = {
        "person_id": {
            "type": "string",
            "minlength": 36,
            "maxlength": 36,
            "required": True,
            "empty": False,
        },
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
    validator = CreatePersonInputDtoValidator(input_data)
    validator.validate()
    validator.verify.assert_called_once_with(schema)


def test_create_person_input_dto_validator_with_invalid_country(
    test_data: Dict[str, str],
) -> None:
    input_data = test_data
    input_data["country"] = "United States"
    validator = CreatePersonInputDtoValidator(input_data)
    with pytest.raises(FieldValueNotPermittedException) as e:
        validator.validate()
    assert str(e.value) == "Country: United States is not a permitted value"


def test_create_person_input_dto_validator_with_invalid_city(
    test_data: Dict[str, str],
) -> None:
    input_data = test_data
    input_data["city"] = "Quito"
    validator = CreatePersonInputDtoValidator(input_data)
    with pytest.raises(FieldValueNotPermittedException) as e:
        validator.validate()
    assert str(e.value) == "City: Quito is not a permitted value"


def test_create_person_input_dto_validator_with_invalid_name(
    test_data: Dict[str, str],
) -> None:
    input_data = test_data
    input_data["name"] = "J"
    validator = CreatePersonInputDtoValidator(input_data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert str(e.value) == "name: min length is 2"


def test_create_person_input_dto_validator_with_empty_values(
    test_data: Dict[str, str],
) -> None:
    input_data = test_data
    input_data["name"] = ""
    input_data["phone"] = ""
    validator = CreatePersonInputDtoValidator(input_data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert (
        str(e.value)
        == "name: empty values not allowed\nphone: empty values not allowed"
    )
