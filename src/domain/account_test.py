from typing import Any, Dict

import pytest

from . import Account


def test_account_creation(fixture_account_data: Dict[str, Any]) -> None:
    account = Account(**fixture_account_data)

    for attr, value in fixture_account_data.items():
        assert getattr(account, attr) == value


def test_from_dict(fixture_account_data: Dict[str, Any]) -> None:
    account = Account.from_dict(fixture_account_data)

    for attr, value in fixture_account_data.items():
        assert getattr(account, attr) == value


def test_to_dict(fixture_account_data: Dict[str, Any]) -> None:
    account = Account.from_dict(fixture_account_data)
    assert account.to_dict() == fixture_account_data


def test_account_comparison(fixture_account_data: Dict[str, Any]) -> None:
    person1 = Account.from_dict(fixture_account_data)
    person2 = Account.from_dict(fixture_account_data)
    assert person1 == person2


def test_account_inequality(fixture_account_data: Dict[str, Any]) -> None:
    person1 = Account.from_dict(fixture_account_data)
    modified_data = fixture_account_data.copy()
    modified_data["email"] = "different_email@gmail.com"
    person2 = Account.from_dict(modified_data)
    assert person1 != person2


def test_missing_required_attribute(fixture_account_data: Dict[str, Any]) -> None:
    del fixture_account_data["email"]
    with pytest.raises(TypeError):
        Account.from_dict(fixture_account_data)
