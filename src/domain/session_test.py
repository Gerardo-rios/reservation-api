from typing import Any, Dict

import pytest

from . import Account, Person, Role, Session


def test_session_creation(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )

    assert session.account == Account(**fixture_account_data)
    assert session.person == Person(**fixture_person_data)
    assert session.role == Role(**fixture_role_data)


def test_from_dict(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session = Session.from_dict(
        {
            "account": fixture_account_data,
            "person": fixture_person_data,
            "role": fixture_role_data,
        }
    )

    assert session.account == fixture_account_data
    assert session.person == fixture_person_data
    assert session.role == fixture_role_data


def test_to_dict(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )

    assert session.to_dict() == {
        "account": fixture_account_data,
        "person": fixture_person_data,
        "role": fixture_role_data,
    }


def test_session_comparison(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session1 = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )
    session2 = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )

    assert session1 == session2


def test_session_inequality(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session1 = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )
    modified_data = {
        "account": fixture_account_data,
        "person": fixture_person_data,
        "role": fixture_role_data,
    }
    modified_data["role"]["role_name"] = "Different Role"
    session2 = Session.from_dict(modified_data)

    assert session1 != session2
