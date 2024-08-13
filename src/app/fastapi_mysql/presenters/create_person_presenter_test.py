from typing import Any, Dict
from src.interactor import CreatePersonOutputDto
from src.domain import Person
from . import CreatePersonPresenter


def test_create_person_presenter(fixture_person_data: Dict[str, Any]) -> None:
    person = Person(**fixture_person_data)
    output_dto = CreatePersonOutputDto(person)
    presenter = CreatePersonPresenter()
    response = presenter.present(output_dto)
    assert response == {
        "person_id": fixture_person_data["person_id"],
        "name": fixture_person_data["name"],
        "phone": fixture_person_data["phone"],
        "city": fixture_person_data["city"],
        "country": fixture_person_data["country"],
    }
