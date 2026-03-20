from fastapi import APIRouter, File, UploadFile, Form

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
    camera_id: str = Form(None),
    food_item: str = Form("Unknown"),
):
    return await compare_food_images(image_a, image_b, camera_id=camera_id, food_item=food_item)
