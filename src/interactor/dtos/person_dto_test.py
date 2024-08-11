from typing import Any, Dict
from . import CreatePersonInputDto


def test_create_person_input_dto(fixture_person_data: Dict[str, Any]) -> None:
    del fixture_person_data["person_id"]
    input_dto = CreatePersonInputDto(**fixture_person_data)

    for attr, value in fixture_person_data.items():
        assert getattr(input_dto, attr) == value
    assert input_dto.to_dict() == fixture_person_data
