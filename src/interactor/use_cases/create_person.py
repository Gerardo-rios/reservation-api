import uuid
from typing import Any, Dict
from src.domain import Person
from src.interactor import (
    CreatePersonInputDto,
    CreatePersonOutputDto,
    CreatePersonPresenterInterface,
    PersonRepositoryInterface,
    CreatePersonInputDtoValidator,
    ItemNotCreatedException,
)


class CreatePersonUseCase:
    def __init__(
        self,
        person_repository: PersonRepositoryInterface,
        presenter: CreatePersonPresenterInterface,
    ):
        self.person_repository = person_repository
        self.presenter = presenter

    def execute(self, input_dto: CreatePersonInputDto) -> Dict[str, Any]:
        validator = CreatePersonInputDtoValidator(input_dto.to_dict())
        validator.validate()
        input_person = Person(
            person_id=uuid.uuid4(),
            name=input_dto.name,
            phone=input_dto.phone,
            address=input_dto.address,
            city=input_dto.city,
            country=input_dto.country,
        )
        person = self.person_repository.create(input_person)
        if person is None:
            raise ItemNotCreatedException(input_dto.name, "person")

        output_dto = CreatePersonOutputDto(person)
        presenter_response = self.presenter.present(output_dto)
        return presenter_response