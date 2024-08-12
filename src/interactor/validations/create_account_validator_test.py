import pytest
from typing import Any, Dict
from pytest_mock import MockFixture
from . import CreateAccountInputDtoValidator
from src.interactor import EmailFormatException, PasswordFormatException


@pytest.fixture
def test_data(
    fixture_account_data: Dict[str, str],
    fixture_rol_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> Dict[str, Any]:
    del fixture_account_data["account_id"]
    del fixture_account_data["status"]
    return {
        **fixture_account_data,
        "rol_id": str(fixture_rol_data["rol_id"]),
        "person_id": str(fixture_person_data["person_id"]),
    }


def test_create_account_input_dto_validator(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    schema = {
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
        "rol_id": {"type": "string", "required": True, "empty": False},
        "person_id": {"type": "string", "required": True, "empty": False},
    }
    validator = CreateAccountInputDtoValidator(input_data)
    validator.validate()
    validator.verify.assert_called_once_with(schema)


def test_create_account_input_dto_validator_with_invalid_email(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    input_data["email"] = "invalid_email"
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(EmailFormatException) as e:
        validator.validate()
    assert str(e.value) == "Email 'invalid_email' has an invalid format"


def test_create_account_input_dto_validator_with_invalid_password(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    input_data["password"] = "invalid_password"
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(PasswordFormatException) as e:
        validator.validate()
    assert str(e.value) == "Password 'invalid_password' has not the required format"


def test_create_account_input_dto_validator_with_empty_values(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    input_data = test_data
    input_data["email"] = ""
    input_data["password"] = ""
    input_data["rol_id"] = ""
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert (
        str(e.value)
        == "email: empty values not allowed\npassword: empty values not allowed\nrol_id: empty values not allowed"  # noqa
    )