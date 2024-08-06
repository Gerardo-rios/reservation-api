from typing import Dict, Any
import pytest

from . import Person


def test_person_creation(fixture_person_data: Dict[str, Any]) -> None:
    person = Person(**fixture_person_data)

    for attr, value in fixture_person_data.items():
        assert getattr(person, attr) == value


def test_from_dict(fixture_person_data: Dict[str, Any]) -> None:
    person = Person.from_dict(fixture_person_data)

    for attr, value in fixture_person_data.items():
        assert getattr(person, attr) == value


def test_to_dict(fixture_person_data: Dict[str, Any]) -> None:
    person = Person.from_dict(fixture_person_data)
    assert person.to_dict() == fixture_person_data


def test_person_comparison(fixture_person_data: Dict[str, Any]) -> None:
    person1 = Person.from_dict(fixture_person_data)
    person2 = Person.from_dict(fixture_person_data)
    assert person1 == person2


def test_person_inequality(fixture_person_data: Dict[str, Any]) -> None:
    person1 = Person.from_dict(fixture_person_data)
    modified_data = fixture_person_data.copy()
    modified_data["name"] = "Different Name"
    person2 = Person.from_dict(modified_data)
    assert person1 != person2


def test_missing_required_attribute(fixture_person_data: Dict[str, Any]) -> None:
    del fixture_person_data["name"]
    with pytest.raises(TypeError):
        Person.from_dict(fixture_person_data)
