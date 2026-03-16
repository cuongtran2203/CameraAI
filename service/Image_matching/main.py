from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from utils import read_image, analyze_food_image, faiss_cosine_similarity

app = FastAPI(title="Food Image Matching API")


class CompareResponse(BaseModel):
    score: float
    is_match: bool
    image_a_caption: str
    image_b_caption: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/compare", response_model=CompareResponse)
async def compare_food_images(
    image_a: UploadFile = File(...),
    image_b: UploadFile = File(...)
):
    bytes_a = await image_a.read()
    bytes_b = await image_b.read()

    pil_a = read_image(bytes_a)
    pil_b = read_image(bytes_b)

    result_a = analyze_food_image(pil_a)
    result_b = analyze_food_image(pil_b)

    score = faiss_cosine_similarity(result_a["fused_vec"], result_b["fused_vec"])

    return CompareResponse(
        score=round(float(score), 4),
        is_match=bool(score >= 0.8),
        image_a_caption=result_a["dense_caption"],
        image_b_caption=result_b["dense_caption"],
    )