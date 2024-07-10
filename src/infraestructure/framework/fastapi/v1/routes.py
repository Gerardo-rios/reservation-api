from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/")
async def index() -> Dict[str, str]:
    return {"message": "Hello World!"}
