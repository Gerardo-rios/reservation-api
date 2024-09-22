from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from configs import config
from src.app.fastapi import routes
from src.infra import db_models

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
    app.title = "Reservations API"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.FRONTEND_DOMAIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes.account_router, prefix=API_PREFIX)

    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, error: HTTPException) -> JSONResponse:
        response = {
            "error": error.__class__.__name__,
            "message": error.detail,
        }
        return JSONResponse(
            status_code=error.status_code,
            content=response,
            headers={"Access-Control-Allow-Origin": config.FRONTEND_DOMAIN},
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, error: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=format_error_response(error, 400),
            headers={"Access-Control-Allow-Origin": config.FRONTEND_DOMAIN},
        )

    @app.exception_handler(Exception)
    async def handle_general_exception(
        request: Request, error: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=format_error_response(error, 500),
            headers={"Access-Control-Allow-Origin": config.FRONTEND_DOMAIN},
        )

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next: Any) -> Any:
        request.state.db = db_models.db_base.Session()
        response = await call_next(request)
        request.state.db.close()
        return response

    return app


def get_db(request: Request) -> db_models.db_base.Session:
    return request.state.db
