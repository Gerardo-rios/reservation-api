from typing import Optional

from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class LoginUseCase:
    def __init__(self, login_repository: interfaces.LoginRepositoryInterface) -> None:
        self.repository = login_repository

    def execute(
        self,
        request_input: request_models.LoginRequest,
        auth_token: Optional[str] = None,
    ) -> response_models.LoginResponse:
        account = self.repository.login(request_input.email, request_input.password)
        if account is None:
            raise errors.AuthenticationError("Invalid email or password provided")

        result = response_models.LoginResponse(
            account=account.account_id, token=auth_token
        )

        return result
