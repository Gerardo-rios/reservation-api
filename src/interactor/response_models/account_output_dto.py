from dataclasses import dataclass


@dataclass
class CreateAccountResponse:
    account_id: str
    person_id: str
    role_id: str
