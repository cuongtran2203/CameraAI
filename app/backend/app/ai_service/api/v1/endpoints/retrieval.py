from fastapi import APIRouter, File, Query, UploadFile, Form

from schemas.retrieval import RetrievalResponse
from services.retrieval import get_default_retrieval_engine

router = APIRouter()

engine = get_default_retrieval_engine()


@router.post("/search", response_model=RetrievalResponse)
async def search_food(
    image: UploadFile = File(...),
    top_k: int = Query(10, ge=1, le=50),
    camera_id: str = Form(None),
):
    image_bytes = await image.read()

    # NOTE: this function expects a PIL Image; the engine will call the VLM and vector encoders.
    from PIL import Image
    import io

    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    return engine.search(pil_img, top_k=top_k, camera_id=camera_id)
