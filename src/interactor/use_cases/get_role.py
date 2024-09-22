from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class GetRoleUseCase:
    def __init__(self, role_repository: interfaces.RoleRepositoryInterface) -> None:
        self.repository = role_repository

    def execute(
        self, request_input: request_models.GetRoleRequest
    ) -> response_models.GetRoleResponse:
        role = self.repository.get(request_input.role_name)
        if role is None:
            raise errors.ItemNotFoundException(request_input.role_name, "role")
        result = response_models.GetRoleResponse(
            role_id=role.role_id, role_name=role.role_name, description=role.description
        )
        return result
