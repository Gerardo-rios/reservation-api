from typing import Dict
from unittest import mock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def fixture_fastapi_app() -> FastAPI:
    with mock.patch("sqlalchemy.create_engine", autospec=True) as mock_create_engine:
        from src.app.fastapi_mysql.create_fast_api_app import create_fastapi_app

        app = create_fastapi_app()
        yield app


@pytest.fixture
def fixture_client_app(fixture_fastapi_app: FastAPI) -> TestClient:
    return TestClient(fixture_fastapi_app)


def test_create_account_request(
    mocker: mock.MagicMock,
    fixture_client_app: TestClient,
    fixture_account_data: Dict[str, str],
    fixture_person_data: Dict[str, str],
    fixture_role_data: Dict[str, str],
):
    input_data = {
        "name": fixture_person_data["name"],
        "phone": fixture_person_data["phone"],
        "address": fixture_person_data["address"],
        "role_name": fixture_role_data["role_name"],
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
        "user": fixture_account_data["user"],
        "photo": fixture_account_data["photo"],
    }

    expected_response_dict = {
        "account_id": fixture_account_data["account_id"],
        "email": fixture_account_data["email"],
        "person_id": fixture_person_data["person_id"],
        "person_name": fixture_person_data["name"],
        "role_id": fixture_role_data["role_id"],
        "message": "Account created successfully",
    }

    controller_mock = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountController",
        autospec=True,
    )

    instance_mock = controller_mock.return_value
    instance_mock.execute.return_value = expected_response_dict

    response = fixture_client_app.post("/api/v1/account/create", json=input_data)

    assert response.status_code == 200
    controller_mock.assert_called_once()
    instance_mock.create_account_request_data.assert_called_once_with(input_data)
