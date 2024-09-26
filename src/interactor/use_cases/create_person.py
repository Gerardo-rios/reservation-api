from dataclasses import asdict
from typing import Optional

from src.domain import interfaces
from src.interactor import errors, request_models, response_models, validations


class CreatePersonUseCase:
    def __init__(self, person_repository: interfaces.PersonRepositoryInterface) -> None:
        self.person_repository = person_repository

    def execute(
        self, request_input: request_models.CreatePersonRequest
    ) -> Optional[response_models.CreatePersonResponse]:
        validator = validations.CreatePersonInputDtoValidator(asdict(request_input))
        validator.validate()
        person = self.person_repository.create(
            name=request_input.name,
            phone=request_input.phone,
            address=request_input.address,
            city=request_input.city,
            country=request_input.country,
        )
        if person is None:
            raise errors.ItemNotCreatedException(request_input.name, "person")

        result = response_models.CreatePersonResponse(person_id=person.person_id)
        return result
