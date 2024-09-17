from typing import Any, Dict

import bcrypt

from src.domain.interfaces import (
    AccountRepositoryInterface,
    CreateAccountPresenterInterface,
)
from src.domain.request_models import CreateAccountInputDto, CreateAccountOutputDto
from src.interactor.errors import ItemNotCreatedException
from src.interactor.validations import CreateAccountInputDtoValidator


class CreateAccountUseCase:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        presenter: CreateAccountPresenterInterface,
    ):
        self.account_repository = account_repository
        self.presenter = presenter

    def execute(self, input_dto: CreateAccountInputDto) -> Dict[str, Any]:
        validator = CreateAccountInputDtoValidator(input_dto.to_dict())
        validator.validate()
        hashed_password = bcrypt.hashpw(
            input_dto.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        account = self.account_repository.create(
            email=input_dto.email,
            password=hashed_password,
            user=input_dto.user,
            photo=input_dto.photo,
            status=True,
            role_id=input_dto.role_id,
            person=input_dto.person,
        )
        if account is None:
            raise ItemNotCreatedException(input_dto.email, "account")

        output_dto = CreateAccountOutputDto(
            account=account, role_id=input_dto.role_id, person=input_dto.person
        )
        presenter_response = self.presenter.present(output_dto)
        return presenter_response
