from typing import List

from pydantic import BaseModel


class ImageAnalysis(BaseModel):
    dense_caption: str
    ingredients: List[str]


class CompareResponse(BaseModel):
    score: float
    base_score: float
    ingredient_score: float
    is_match: bool
    image_a: ImageAnalysis
    image_b: ImageAnalysis
