from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.app.fastapi_mysql.controllers.account_creation_controller import (
    CreateAccountController,
)
from src.app.fastapi_mysql.controllers.login_account_controller import (
    LoginAccountController,
)
from src.interactor.dtos import LoginInputDto

account_router = APIRouter()


@account_router.post("/account/create", status_code=201)
async def create_account(
    json_input_data: Dict[str, str],
    controller: CreateAccountController = Depends(CreateAccountController),
) -> JSONResponse:
    controller.create_request_data(json_input_data)
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)


@account_router.post("/account/login", status_code=200)
async def login_account(
    json_input_data: LoginInputDto,
    controller: LoginAccountController = Depends(LoginAccountController),
) -> JSONResponse:
    controller.create_request_data(json_input_data.to_dict())
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)
