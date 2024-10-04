from src.domain import interfaces
from src.interactor import errors, request_models, response_models


class GetAccountUseCase:
    def __init__(
        self, account_repository: interfaces.AccountRepositoryInterface
    ) -> None:
        self.repository = account_repository

    def execute(
        self, request_input: request_models.GetAccountByIdRequest
    ) -> response_models.GetAccountResponse:
        account = self.repository.get(request_input.account_id)
        if account is None:
            raise errors.ItemNotFoundException(request_input.account_id, "account")
        result = response_models.GetAccountResponse(
            account=account["account"],
            person_id=account["person_id"],
            role_id=account["role_id"],
        )
        return result
