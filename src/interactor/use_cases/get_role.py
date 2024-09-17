from typing import Any, Dict

from src.domain.interfaces import GetRolePresenterInterface, RoleRepositoryInterface
from src.domain.request_models import GetRoleInputDto, GetRoleOutputDto
from src.interactor.errors import ItemNotFoundException


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
