from fastapi.testclient import TestClient
from . import create_fastapi_app

app = create_fastapi_app()
client = TestClient(app)


def test_call_hello_world() -> None:
    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
