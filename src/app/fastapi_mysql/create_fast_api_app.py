from typing import Any, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from . import account_router
from src import Session as DbSession


API_PREFIX = "/api/v1"


def format_error_response(error: Exception, error_code: int) -> Dict[str, Any]:
    response = {
        "status_code": error_code,
        "error": error.__class__.__name__,
        "message": str(error),
    }
    return response


def create_fastapi_app() -> FastAPI:
    app = FastAPI()

    app.include_router(account_router, prefix=API_PREFIX)

    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, error: HTTPException) -> JSONResponse:
        response = {
            "error": error.__class__.__name__,
            "message": error.detail,
        }
        return JSONResponse(status_code=error.status_code, content=response)

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, error: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content=format_error_response(error, 400))

    @app.exception_handler(Exception)
    async def handle_general_exception(
        request: Request, error: Exception
    ) -> JSONResponse:
        return JSONResponse(status_code=500, content=format_error_response(error, 500))

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next: Any) -> Any:
        request.state.db = DbSession()
        response = await call_next(request)
        request.state.db.close()
        return response

    return app


def get_db(request: Request) -> DbSession:
    return request.state.db
