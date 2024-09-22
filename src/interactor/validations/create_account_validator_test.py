from typing import Any, Dict

import pytest
from pytest_mock import MockFixture

from src.interactor import errors

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
        "role_id": fixture_role_data["role_id"],
        "person_id": fixture_person_data["person_id"],
    }


def test__create_account_input_dto_validator__does_not_raise_a_error__when_successfully_validates(  # noqa
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
        "person_id": {"type": "string", "required": True, "empty": False},
    }
    validator = CreateAccountInputDtoValidator(test_data)
    validator.validate()
    validator.verify.assert_any_call(schema)
    validator.verify.call_count == 1


def test__create_account_input_dto_validator__raises_an_error__when_invalid_email_is_provided(  # noqa
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    input_data["email"] = "invalid_email"
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(errors.EmailFormatException) as e:
        validator.validate()
    assert str(e.value) == "Email 'invalid_email' has an invalid format"


def test__create_account_input_dto_validator__raises_error__when_password_is_invalid(
    test_data: Dict[str, Any], mocker: MockFixture
) -> None:
    mocker.patch(
        "src.interactor.validations.base_input_validator.BaseInputValidator.verify"
    )
    input_data = test_data
    input_data["password"] = "invalid_password"
    validator = CreateAccountInputDtoValidator(input_data)
    with pytest.raises(errors.PasswordFormatException) as e:
        validator.validate()
    assert str(e.value) == "Password 'invalid_password' has not the required format"


def test__create_account_input_dto_validator__raises_error__when_input_fields_are_empty(
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
