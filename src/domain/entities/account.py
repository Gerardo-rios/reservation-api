from dataclasses import dataclass


@dataclass
class Account:
    account_id: str
    email: str
    password: str
    user: str
    photo: str
    status: bool
