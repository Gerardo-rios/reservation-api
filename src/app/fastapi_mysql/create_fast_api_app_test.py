from typing import Dict
from fastapi.testclient import TestClient
from fastapi import HTTPException, Request
from src.app.fastapi_mysql.create_fast_api_app import create_fastapi_app, get_db
from unittest.mock import Mock

app = create_fastapi_app()
client = TestClient(app)


def test_app_creation() -> None:
    assert app.title == "Reservations API"


def test_http_exception_handler() -> None:
    @app.get("/http_exception")
    async def raise_http_exception() -> None:
        raise HTTPException(status_code=404, detail="Not Found")

    response = client.get("/http_exception")
    assert response.status_code == 404
    assert response.json() == {"error": "HTTPException", "message": "Not Found"}


def test_value_error_handler() -> None:
    @app.get("/value_error")
    async def raise_value_error() -> None:
        raise ValueError("Invalid value")

    response = client.get("/value_error")
    assert response.status_code == 400
    assert response.json() == {
        "status_code": 400,
        "error": "ValueError",
        "message": "Invalid value",
    }


def test_db_session_middleware(mocker: Mock) -> None:
    mock_db_session = mocker.patch(
        "src.app.fastapi_mysql.create_fast_api_app.DbSession", autospec=True
    )

    @app.get("/test_db")
    async def test_db(request: Request) -> Dict[str, str]:
        db = get_db(request)
        assert db is not None
        return {"message": "DB session is active"}

    response = client.get("/test_db")
    assert response.status_code == 200
    assert response.json() == {"message": "DB session is active"}
    mock_db_session.assert_called_once()
    mock_db_session.return_value.close.assert_called_once()
