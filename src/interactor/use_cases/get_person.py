from typing import Optional

from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class GetPersonUseCase:
    def __init__(self, person_repository: interfaces.PersonRepositoryInterface) -> None:
        self.repository = person_repository

    def execute(
        self, request_input: request_models.GetPersonByPhoneRequest
    ) -> Optional[response_models.GetPersonResponse]:
        person = self.repository.get_by_phone(request_input.phone)
        if person is None:
            raise errors.ItemNotFoundException(request_input.phone, "person")
        result = response_models.GetPersonResponse(
            person_id=person.person_id,
            name=person.name,
            phone=person.phone,
            address=person.address,
            city=person.city,
            country=person.country,
        )
        return result
