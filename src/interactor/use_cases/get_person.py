from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class GetPersonUseCase:
    def __init__(self, person_repository: interfaces.PersonRepositoryInterface) -> None:
        self.repository = person_repository

    def execute(
        self, request_input: request_models.GetPersonRequest
    ) -> response_models.GetPersonResponse:
        person = None
        if request_input.person_id:
            person = self.repository.get_by_id(request_input.person_id)
        if person is None and request_input.phone:
            person = self.repository.get_by_phone(request_input.phone)

        if person is None:
            search_param = request_input.person_id or request_input.phone
            raise errors.ItemNotFoundException(search_param, "person")  # type: ignore

        return response_models.GetPersonResponse(
            person_id=person.person_id,
            name=person.name,
            phone=person.phone,
            address=person.address,
            city=person.city,
            country=person.country,
        )
