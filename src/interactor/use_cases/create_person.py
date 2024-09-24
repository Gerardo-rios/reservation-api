from typing import Dict, Optional

from src.domain import interfaces


class CreatePersonUseCase:
    def __init__(self, person_repository: interfaces.PersonRepositoryInterface) -> None:
        self.repository = person_repository

    def execute(self) -> Optional[Dict[str, str]]:
        pass
