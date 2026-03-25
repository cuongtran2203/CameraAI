from fastapi import UploadFile

from core.config import W_BASE, W_INGREDIENT
from schemas.match import CompareResponse, ImageAnalysis
from vision import (
    analyze_food_image,
    faiss_cosine_similarity,
    ingredient_similarity,
    read_image,
)


async def compare_food_images(image_a: UploadFile, image_b: UploadFile) -> CompareResponse:
    bytes_a = await image_a.read()
    bytes_b = await image_b.read()

    pil_a = read_image(bytes_a)
    pil_b = read_image(bytes_b)

    result_a = analyze_food_image(pil_a)
    result_b = analyze_food_image(pil_b)

    base_score = faiss_cosine_similarity(result_a["fused_vec"], result_b["fused_vec"])
    ing_score = ingredient_similarity(result_a["ingredients"], result_b["ingredients"])

    final_score = (W_BASE * base_score) + (W_INGREDIENT * ing_score)

    return CompareResponse(
        score=round(float(final_score), 4),
        base_score=round(float(base_score), 4),
        ingredient_score=round(float(ing_score), 4),
        is_match=bool(final_score >= 0.75),
        image_a=ImageAnalysis(
            dense_caption=result_a["dense_caption"],
            ingredients=result_a["ingredients"],
        ),
        image_b=ImageAnalysis(
            dense_caption=result_b["dense_caption"],
            ingredients=result_b["ingredients"],
        ),
    )
