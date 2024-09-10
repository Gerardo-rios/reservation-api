from typing import Any, Dict

from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.interactor.request_models import LoginInputDto, LoginOutputDto


class LoginUseCase:
    def __init__(
        self,
        login_repository: LoginRepositoryInterface,
        login_presenter: LoginPresenterInterface,
    ) -> None:
        self.repository = login_repository
        self.presenter = login_presenter

    def execute(self, input_dto: LoginInputDto) -> Dict[str, Any]:
        account = self.repository.login(input_dto.email, input_dto.password)
        if account is None:
            raise AuthenticationError("Invalid email or password provided")

        output_login_dto = LoginOutputDto(account=account.account_id)

        return self.presenter.present(output_login_dto)
