class ItemNotFoundException(Exception):
    def __init__(self, item: str, item_type: str) -> None:
        self.item = item
        self.item_type = item_type
        super().__init__(f"{self.item_type.capitalize()} '{self.item}' was not found")


class AuthenticationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
