from fastapi import APIRouter
from api.v1.endpoints import match

api_router = APIRouter()
api_router.include_router(match.router, prefix="/match", tags=["match"])
