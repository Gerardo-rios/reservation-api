from fastapi import APIRouter, Depends, status
from typing import Dict
from src.app.fastapi_mysql.controllers.account_creation_controller import (
    CreateAccountController,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

account_router = APIRouter()


@account_router.post("/account/create", status_code=status.HTTP_201_CREATED)
async def create_account(
    json_input_data: Dict[str, str],
    controller: CreateAccountController = Depends(CreateAccountController),
) -> JSONResponse:
    controller.create_account_request_data(json_input_data)
    controller_response = controller.execute()
    json_response = jsonable_encoder(controller_response)
    return JSONResponse(content=json_response)
