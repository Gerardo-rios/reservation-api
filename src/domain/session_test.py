from typing import Any, Dict

import pytest

from . import LoginSession


@pytest.fixture
def test_data(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "account": {
            "account_id": fixture_account_data["account_id"],
            "email": fixture_account_data["email"],
            "user": fixture_account_data["user"],
            "photo": fixture_account_data["photo"],
        },
        "person": {
            "person_id": fixture_person_data["person_id"],
            "name": fixture_person_data["name"],
            "phone": fixture_person_data["phone"],
            "address": fixture_person_data["address"],
        },
        "role": {
            "role_id": fixture_role_data["role_id"],
            "role_name": fixture_role_data["role_name"],
        },
    }


def test_session_creation(
    test_data: Dict[str, Any],
) -> None:
    session = LoginSession(
        account=test_data["account"],
        person=test_data["person"],
        role=test_data["role"],
    )

    assert session.account == test_data["account"]
    assert session.person == test_data["person"]
    assert session.role == test_data["role"]


def test_from_dict(
    test_data: Dict[str, Any],
) -> None:
    session = LoginSession.from_dict(test_data)

    assert session.account == test_data["account"]
    assert session.person == test_data["person"]
    assert session.role == test_data["role"]


def test_to_dict(
    test_data: Dict[str, Any],
) -> None:
    session = LoginSession(
        account=test_data["account"], person=test_data["person"], role=test_data["role"]
    )

    assert session.to_dict() == {
        "account": test_data["account"],
        "person": test_data["person"],
        "role": test_data["role"],
    }


def test_session_comparison(
    test_data: Dict[str, Any],
) -> None:
    session1 = LoginSession(
        account=test_data["account"],
        person=test_data["person"],
        role=test_data["role"],
    )
    session2 = LoginSession(
        account=test_data["account"],
        person=test_data["person"],
        role=test_data["role"],
    )

    assert session1 == session2


def test_session_inequality(
    test_data: Dict[str, Any],
) -> None:
    session1 = LoginSession(
        account=test_data["account"],
        person=test_data["person"],
        role=test_data["role"],
    )
    modified_data = {
        "account": test_data["account"],
        "person": test_data["person"],
        "role": {
            "role_id": "test_role_id",
            "role_name": "Different Role",
        },
    }
    session2 = LoginSession.from_dict(modified_data)

    assert session1 != session2
