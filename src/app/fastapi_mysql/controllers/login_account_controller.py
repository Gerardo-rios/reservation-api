from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from configs.config import SECRET_KEY
from src.app.fastapi_mysql.interfaces import AccountControllerInterface
from src.app.fastapi_mysql.response_models import LoginAccountPresenter
from src.infra import LoginMySQLRepository
from src.interactor.request_models import LoginInputDto
from src.interactor.use_cases import LoginUseCase

from .controllers_utils import validate_input_keys


class LoginAccountController(AccountControllerInterface):
    TOKEN_EXPIRATION_MINUTES = 120
    TOKEN_ALGORITHM = "HS256"

    def __init__(self) -> None:
        self.input_login_dto: LoginInputDto

    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        valid_keys = ["email", "password"]
        validate_input_keys(json_input_data, valid_keys)

        self.input_login_dto = LoginInputDto(
            email=json_input_data["email"], password=json_input_data["password"]
        )

    def execute(self) -> Dict[str, Any]:
        repository = LoginMySQLRepository()
        presenter = LoginAccountPresenter()
        use_case = LoginUseCase(
            login_repository=repository,
            login_presenter=presenter,
        )
        auth_token = self.__generate_jwt_session_token(self.input_login_dto.email)
        result = use_case.execute(input_dto=self.input_login_dto, auth_token=auth_token)
        return result

    def __generate_jwt_session_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.TOKEN_EXPIRATION_MINUTES),
        }
        token = str(jwt.encode(payload, SECRET_KEY, algorithm=self.TOKEN_ALGORITHM))
        return token
