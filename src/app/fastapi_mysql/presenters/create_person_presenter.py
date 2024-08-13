from typing import Any, Dict
from src.interactor import CreatePersonOutputDto, CreatePersonPresenterInterface


class CreatePersonPresenter(CreatePersonPresenterInterface):
    def present(self, response: CreatePersonOutputDto) -> Dict[str, Any]:
        return {
            "person_id": response.person.person_id,
            "name": response.person.name,
            "phone": response.person.phone,
            "city": response.person.city,
            "country": response.person.country,
        }
