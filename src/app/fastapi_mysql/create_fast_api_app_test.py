# from fastapi.testclient import TestClient
# from . import create_fastapi_app

# app = create_fastapi_app()
# client = TestClient(app)


# def test_create_account():
#     response = client.post(
#         "/api/v1/account/create",
#         json={
#             "name": "John Doe",
#             "email": "test_mail@gmail.com",
#             "password": "Str0ngP@ss!",
#             "user": "test_user",
#             "photo": "test_photo",
#             "phone": "1234567890",
#             "address": "1234 Elm St",
#             "rol": "admin"
#         },
#     )

#     print(response.json())

#     assert response.status_code == 201
