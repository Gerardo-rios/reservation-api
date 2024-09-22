from dataclasses import dataclass


@dataclass
class GetRoleRequest:
    role_name: str
