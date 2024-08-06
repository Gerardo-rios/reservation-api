from typing import Dict, Any
import pytest

from . import Rol


def test_rol_creation(fixture_rol_data: Dict[str, Any]) -> None:
    rol = Rol(**fixture_rol_data)

    for attr, value in fixture_rol_data.items():
        assert getattr(rol, attr) == value


def test_from_dict(fixture_rol_data: Dict[str, Any]) -> None:
    rol = Rol.from_dict(fixture_rol_data)

    for attr, value in fixture_rol_data.items():
        assert getattr(rol, attr) == value


def test_to_dict(fixture_rol_data: Dict[str, Any]) -> None:
    rol = Rol.from_dict(fixture_rol_data)
    assert rol.to_dict() == fixture_rol_data


def test_rol_comparison(fixture_rol_data: Dict[str, Any]) -> None:
    person1 = Rol.from_dict(fixture_rol_data)
    person2 = Rol.from_dict(fixture_rol_data)
    assert person1 == person2


def test_rol_inequality(fixture_rol_data: Dict[str, Any]) -> None:
    person1 = Rol.from_dict(fixture_rol_data)
    modified_data = fixture_rol_data.copy()
    modified_data["rol_name"] = "Different Rol"
    person2 = Rol.from_dict(modified_data)
    assert person1 != person2


def test_missing_required_attribute(fixture_rol_data: Dict[str, Any]) -> None:
    del fixture_rol_data["rol_name"]
    with pytest.raises(TypeError):
        Rol.from_dict(fixture_rol_data)
