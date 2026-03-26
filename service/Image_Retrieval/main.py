from typing import List

from fastapi import FastAPI, File, Query, UploadFile
from pydantic import BaseModel

from retrieval import FoodRetrievalEngine
from utils import read_image

app = FastAPI(title="Food Retrieval API")

engine = FoodRetrievalEngine(
    index_path="data/faiss.index",
    metadata_path="data/metadata.json",
)


class RetrievalItem(BaseModel):
    id: str
    image_path: str
    description: str
    ingredients: List[str]
    base_score: float
    ingredient_score: float
    score: float


class RetrievalResponse(BaseModel):
    query_description: str
    query_ingredients: List[str]
    top_k: List[RetrievalItem]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=RetrievalResponse)
async def search_food(
    image: UploadFile = File(...),
    top_k: int = Query(10, ge=1, le=50),
):
    image_bytes = await image.read()
    pil_img = read_image(image_bytes)
    return engine.search(pil_img, top_k=top_k)