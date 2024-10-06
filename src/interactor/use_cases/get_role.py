from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class GetRoleUseCase:
    def __init__(self, role_repository: interfaces.RoleRepositoryInterface) -> None:
        self.repository = role_repository

    def execute(
        self, request_input: request_models.GetRoleRequest
    ) -> response_models.GetRoleResponse:
        role = None
        if request_input.role_id:
            role = self.repository.get_by_id(request_input.role_id)
        elif request_input.role_name:
            role = self.repository.get_by_name(request_input.role_name)

        if role is None:
            search_param = request_input.role_id or request_input.role_name
            raise errors.ItemNotFoundException(search_param, "Role")  # type: ignore

        result = response_models.GetRoleResponse(
            role_id=role.role_id, role_name=role.role_name, description=role.description
        )
        return result
