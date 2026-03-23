from fastapi import APIRouter, File, UploadFile

from schemas.match import CompareResponse
from services.matcher import compare_food_images

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/compare", response_model=CompareResponse)
async def compare_images(
    image_a: UploadFile = File(...),
    image_b: UploadFile = File(...),
):
    return await compare_food_images(image_a, image_b)
