from typing import Any, Dict

import pytest
from pytest_mock import MockFixture

from src.interactor import EmailFormatException, PasswordFormatException

from . import CreateAccountInputDtoValidator


@pytest.fixture
def test_data(
    fixture_account_data: Dict[str, str],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> Dict[str, Any]:
    del fixture_account_data["account_id"]
    del fixture_account_data["status"]
    return {
        **fixture_account_data,
        "role_id": str(fixture_role_data["role_id"]),
        "person": fixture_person_data,
    }


def test_create_account_input_dto_validator(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
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
        "role_id": {"type": "string", "required": True, "empty": False},
        "person": {"type": "dict", "required": True, "empty": False},
    }
    validator = CreateAccountInputDtoValidator(test_data)
    validator.validate()
    validator.verify.assert_any_call(schema)
    validator.verify.call_count == 2


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
    input_data["role_id"] = ""
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(ValueError) as e:
        validator.validate()
    assert (
        str(e.value)
        == "email: empty values not allowed\npassword: empty values not allowed\nrole_id: empty values not allowed"  # noqa
    )
