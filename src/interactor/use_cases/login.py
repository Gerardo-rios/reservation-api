from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from configs.config import SECRET_KEY
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.interactor.request_models import LoginInputDto, LoginOutputDto


class LoginUseCase:
    TOKEN_EXPIRATION_MINUTES = 120
    TOKEN_ALGORITHM = "HS256"

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

        token = self.__generate_jwt_session_token(session.account["email"])

        session.token = token

        output_login_dto = LoginOutputDto(token=token, session=session)

        return self.presenter.present(output_login_dto)

    def __generate_jwt_session_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.TOKEN_EXPIRATION_MINUTES),
        }
        token = str(jwt.encode(payload, SECRET_KEY, algorithm=self.TOKEN_ALGORITHM))
        return token
