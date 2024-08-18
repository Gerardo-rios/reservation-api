from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from configs.config import SECRET_KEY
from src.interactor.dtos import LoginInputDto, LoginOutputDto
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface


class LoginUseCase:
    def __init__(
        self,
        login_repository: LoginRepositoryInterface,
        login_presenter: LoginPresenterInterface,
    ) -> None:
        self.repository = login_repository
        self.presenter = login_presenter

    def execute(self, input_dto: LoginInputDto) -> Dict[str, Any]:
        session = self.repository.login(input_dto.email, input_dto.password)
        if session is None:
            raise AuthenticationError("Invalid email or password provided")

        token = self.__generate_jwt_session_token(session.account.email)

        session.token = token

        output_login_dto = LoginOutputDto(token=token, session=session)

        return self.presenter.present(output_login_dto)

    def __generate_jwt_session_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=120),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
