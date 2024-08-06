import uuid
import pytest
from typing import Dict, Any


@pytest.fixture
def fixture_person_data() -> Dict[str, Any]:
    return {
        "person_id": uuid.uuid4(),
        "name": "John Doe",
        "phone": "1234567890",
        "address": "1234 Elm St",
        "city": "Loja",
        "country": "EC",
    }


@pytest.fixture
def fixture_rol_data() -> Dict[str, Any]:
    return {
        "rol_id": uuid.uuid4(),
        "rol_name": "Admin",
        "description": "Admin role",
    }


@pytest.fixture
def fixture_account_data() -> Dict[str, Any]:
    return {
        "account_id": uuid.uuid4(),
        "email": "test_mail@gmail.com",
        "password": "test_password",
        "user": "test_user",
        "photo": "test_photo",
    }
