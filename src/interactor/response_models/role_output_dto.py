from dataclasses import dataclass


@dataclass
class GetRoleResponse:
    role_id: str
    role_name: str
    description: str
