from typing import Any, Dict

from src.interactor.interfaces import GetRolePresenterInterface
from src.interactor.request_models import GetRoleOutputDto


class GetRolePresenter(GetRolePresenterInterface):
    def present(self, response: GetRoleOutputDto) -> Dict[str, Any]:
        return {
            "role_id": response.role.role_id,
            "role_name": response.role.role_name,
            "description": response.role.description,
        }
