from dataclasses import asdict

import bcrypt

from src.domain import interfaces
from src.interactor import errors, request_models, response_models, validations


class CreateAccountUseCase:
    def __init__(
        self,
        account_repository: interfaces.AccountRepositoryInterface,
    ):
        self.account_repository = account_repository

    def execute(
        self, input_data: request_models.CreateAccountRequest
    ) -> response_models.CreateAccountResponse:
        validator = validations.CreateAccountInputDtoValidator(asdict(input_data))
        validator.validate()
        hashed_password = bcrypt.hashpw(
            input_data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        account = self.account_repository.create(
            email=input_data.email,
            password=hashed_password,
            user=input_data.user,
            photo=input_data.photo,
            status=True,
            role_id=input_data.role_id,
            person_id=input_data.person_id,
        )
        if account is None:
            raise errors.ItemNotCreatedException(input_data.email, "account")

        result = response_models.CreateAccountResponse(
            account_id=account.account_id,
            role_id=input_data.role_id,
            person_id=input_data.person_id,
        )
        return result
