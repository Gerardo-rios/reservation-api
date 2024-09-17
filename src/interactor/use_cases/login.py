from typing import Any, Dict, Optional

from src.domain.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.domain.request_models import LoginInputDto, LoginOutputDto
from src.interactor.errors import AuthenticationError


class LoginUseCase:
    def __init__(
        self,
        login_repository: LoginRepositoryInterface,
        login_presenter: LoginPresenterInterface,
    ) -> None:
        self.repository = login_repository
        self.presenter = login_presenter

    def execute(
        self, input_dto: LoginInputDto, auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        account = self.repository.login(input_dto.email, input_dto.password)
        if account is None:
            raise AuthenticationError("Invalid email or password provided")

        output_login_dto = LoginOutputDto(account=account.account_id)

        return self.presenter.present(output_dto=output_login_dto, token=auth_token)
