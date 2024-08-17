from typing import Dict, Any
import pytest

from . import Role


def test_rol_creation(fixture_role_data: Dict[str, Any]) -> None:
    rol = Role(**fixture_role_data)

    for attr, value in fixture_role_data.items():
        assert getattr(rol, attr) == value


def test_from_dict(fixture_role_data: Dict[str, Any]) -> None:
    rol = Role.from_dict(fixture_role_data)

    for attr, value in fixture_role_data.items():
        assert getattr(rol, attr) == value


def test_to_dict(fixture_role_data: Dict[str, Any]) -> None:
    rol = Role.from_dict(fixture_role_data)
    assert rol.to_dict() == fixture_role_data


def test_rol_comparison(fixture_role_data: Dict[str, Any]) -> None:
    person1 = Role.from_dict(fixture_role_data)
    person2 = Role.from_dict(fixture_role_data)
    assert person1 == person2


def test_rol_inequality(fixture_role_data: Dict[str, Any]) -> None:
    person1 = Role.from_dict(fixture_role_data)
    modified_data = fixture_role_data.copy()
    modified_data["role_name"] = "Different Role"
    person2 = Role.from_dict(modified_data)
    assert person1 != person2


def test_missing_required_attribute(fixture_role_data: Dict[str, Any]) -> None:
    del fixture_role_data["role_name"]
    with pytest.raises(TypeError):
        Role.from_dict(fixture_role_data)
