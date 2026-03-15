import json
from pathlib import Path
from typing import List, Dict, Any

import faiss
import numpy as np

from config import W_BASE, W_INGREDIENT
from utils import (
    read_image,
    encode_image,
    encode_text,
    encode_text_list,
    fuse_features,
    ingredient_similarity,
    call_vlm_vision,
)


class FoodRetrievalEngine:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, image, top_k: int = 10, top_n_rerank: int = 50) -> Dict[str, Any]:
        # Analyze query
        vlm_result = call_vlm_vision(image)
        dense_caption = vlm_result["dense_caption"]
        ingredients = vlm_result["ingredients"]

        image_vec = encode_image(image)
        dense_vec = encode_text(dense_caption)
        sparse_vec = encode_text(", ".join(ingredients))
        fused_vec = fuse_features(image_vec, dense_vec, sparse_vec).astype("float32").reshape(1, -1)

        faiss.normalize_L2(fused_vec)

        # Stage 1: coarse retrieval
        scores, indices = self.index.search(fused_vec, top_n_rerank)

        candidates = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = self.metadata[idx]

            ing_score = ingredient_similarity(ingredients, item.get("ingredients", []))
            final_score = (W_BASE * float(score)) + (W_INGREDIENT * ing_score)

            candidates.append({
                "id": item["id"],
                "image_path": item["image_path"],
                "description": item.get("description", ""),
                "ingredients": item.get("ingredients", []),
                "base_score": round(float(score), 4),
                "ingredient_score": round(float(ing_score), 4),
                "score": round(float(final_score), 4),
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query_description": dense_caption,
            "query_ingredients": ingredients,
            "top_k": candidates[:top_k]
        }