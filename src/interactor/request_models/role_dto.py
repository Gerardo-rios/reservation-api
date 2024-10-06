from dataclasses import dataclass
from typing import Optional


@dataclass
class GetRoleRequest:
    role_id: Optional[str] = None
    role_name: Optional[str] = None
