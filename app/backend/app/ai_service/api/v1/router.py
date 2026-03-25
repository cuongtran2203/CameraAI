from fastapi import APIRouter

from .endpoints.match import router as match_router
from .endpoints.retrieval import router as retrieval_router

router = APIRouter(prefix="/v1")
router.include_router(match_router)
router.include_router(retrieval_router)
