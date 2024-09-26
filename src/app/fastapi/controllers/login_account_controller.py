from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from configs.config import SECRET_KEY
from src.app.fastapi import interfaces
from src.infra import repositories
from src.interactor import request_models, response_models, use_cases

from . import controllers_utils


class LoginAccountController(interfaces.LoginControllerInterface):
    TOKEN_EXPIRATION_MINUTES = 120
    TOKEN_ALGORITHM = "HS256"

    def __init__(self) -> None:
        self.input_login_dto: request_models.LoginRequest

    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        valid_keys = ["email", "password"]
        controllers_utils.validate_input_keys(json_input_data, valid_keys)

        self.input_login_dto = request_models.LoginRequest(
            email=json_input_data["email"], password=json_input_data["password"]
        )

    def execute(self) -> response_models.LoginResponse:
        repository = repositories.LoginMySQLRepository()
        use_case = use_cases.LoginUseCase(login_repository=repository)
        auth_token = self.__generate_jwt_session_token(self.input_login_dto.email)
        response = use_case.execute(
            request_input=self.input_login_dto, auth_token=auth_token
        )
        return response

    def __generate_jwt_session_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.TOKEN_EXPIRATION_MINUTES),
        }
        token = str(jwt.encode(payload, SECRET_KEY, algorithm=self.TOKEN_ALGORITHM))
        return token
