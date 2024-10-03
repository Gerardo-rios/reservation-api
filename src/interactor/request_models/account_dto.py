from dataclasses import dataclass

@dataclass
class CreateAccountRequest:
    email: str
    password: str
    user: str
    photo: str
    role_id: str
    person_id: str


@dataclass
class GetAccountByIdRequest:
    account_id: str