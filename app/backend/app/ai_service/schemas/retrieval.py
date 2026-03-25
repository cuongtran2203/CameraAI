from typing import List

from pydantic import BaseModel


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
