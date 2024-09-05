from typing import Any, Dict

from src.interactor.errors import ItemNotFoundException
from src.interactor.interfaces import GetRolePresenterInterface, RoleRepositoryInterface
from src.interactor.request_models import GetRoleInputDto, GetRoleOutputDto


class GetRoleUseCase:
    def __init__(
        self,
        role_repository: RoleRepositoryInterface,
        role_presenter: GetRolePresenterInterface,
    ) -> None:
        self.repository = role_repository
        self.presenter = role_presenter

    def execute(self, input_dto: GetRoleInputDto) -> Dict[str, Any]:
        role = self.repository.get(input_dto.role_name)
        if role is None:
            raise ItemNotFoundException(input_dto.role_name, "role")
        output_dto = GetRoleOutputDto(role)
        return self.presenter.present(output_dto)
