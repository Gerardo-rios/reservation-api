class FieldValueNotPermittedException(Exception):
    def __init__(self, field_name: str, field_value: str) -> None:
        self.field_name = field_name
        self.field_value = field_value

    def __str__(self) -> str:
        return f"""
            {self.field_name.capitalize()}: {self.field_value} is not a permitted value
        """


class ItemNotCreatedException(Exception):
    def __init__(self, item_name: str, item_type: str) -> None:
        self.item_name = item_name
        self.item_type = item_type

    def __str__(self) -> str:
        return f"{self.item_type.capitalize()} '{self.item_name}' was not created"


class EmailFormatException(Exception):
    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f"Email '{self.email}' has an invalid format"


class PasswordFormatException(Exception):
    def __init__(self, password: str) -> None:
        self.password = password

    def __str__(self) -> str:
        return f"Password '{self.password}' has not the required format"
