from dataclasses import asdict
from typing import Any, Dict

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.app.fastapi import controllers, middleware
from src.interactor import request_models

account_router = APIRouter()


@account_router.post("/account/create", status_code=201)
async def create_account(
    json_input_data: Dict[str, str],
    controller: controllers.CreateAccountController = Depends(
        controllers.CreateAccountController
    ),
) -> JSONResponse:
    controller.create_request_data(json_input_data)
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)


@account_router.post("/account/login", status_code=200)
async def login_account(
    json_input_data: request_models.LoginRequest,
    controller: controllers.LoginAccountController = Depends(
        controllers.LoginAccountController
    ),
) -> JSONResponse:
    controller.create_request_data(asdict(json_input_data))
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)


@account_router.get("/account/{account_id}", status_code=200)
async def get_account_data(
    account_id: str,
    controller: controllers.GetAccountDataController = Depends(
        controllers.GetAccountDataController
    ),
    token_payload: Dict[str, Any] = Depends(middleware.verify_jwt_token),
) -> JSONResponse:
    controller.create_request_data({"account_id": account_id})
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)
