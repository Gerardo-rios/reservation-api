from fastapi import FastAPI
from .v1 import router

app = FastAPI()

APP_PREFIX = "/api/v1"

app.include_router(router=router, prefix=APP_PREFIX)
