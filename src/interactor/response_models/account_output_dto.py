from dataclasses import dataclass

from src.domain import entities


@dataclass
class CreateAccountResponse:
    account_id: str
    person_id: str
    role_id: str


@dataclass
class GetAccountResponse:
    account: entities.Account
    person_id: str
    role_id: str
