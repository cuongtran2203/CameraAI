import json
from typing import Any, Dict, List

import faiss
import numpy as np

from config import DEFAULT_TOP_K, TOP_N_RERANK, W_BASE, W_INGREDIENT
from utils import call_vlm_vision, encode_image, encode_text, encode_text_list, fuse_features


def ingredient_similarity_from_vectors(
    query_ingredient_vecs: List[np.ndarray],
    db_ingredient_vecs: List[List[float]],
) -> float:
    if not query_ingredient_vecs or not db_ingredient_vecs:
        return 0.0

    mat_a = np.stack(query_ingredient_vecs).astype("float32")
    mat_b = np.array(db_ingredient_vecs, dtype="float32")

    if mat_a.size == 0 or mat_b.size == 0:
        return 0.0

    faiss.normalize_L2(mat_a)
    faiss.normalize_L2(mat_b)

    index_b = faiss.IndexFlatIP(mat_b.shape[1])
    index_b.add(mat_b)
    scores_ab, _ = index_b.search(mat_a, 1)

    index_a = faiss.IndexFlatIP(mat_a.shape[1])
    index_a.add(mat_a)
    scores_ba, _ = index_a.search(mat_b, 1)

    return float((scores_ab.mean() + scores_ba.mean()) / 2.0)


class FoodRetrievalEngine:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        if self.index.ntotal != len(self.metadata):
            raise RuntimeError(
                f"FAISS index size ({self.index.ntotal}) != metadata size ({len(self.metadata)})"
            )

    def search(
        self,
        image,
        top_k: int = DEFAULT_TOP_K,
        top_n_rerank: int = TOP_N_RERANK,
    ) -> Dict[str, Any]:
        vlm_result = call_vlm_vision(image)
        query_description = vlm_result["dense_caption"]
        query_ingredients = vlm_result["ingredients"]

        image_vec = encode_image(image)
        dense_vec = encode_text(query_description)
        sparse_vec = encode_text(", ".join(query_ingredients))

        query_fused_vec = (
            fuse_features(image_vec, dense_vec, sparse_vec)
            .astype("float32")
            .reshape(1, -1)
        )
        faiss.normalize_L2(query_fused_vec)

        query_ingredient_vecs = encode_text_list(query_ingredients)

        search_k = min(top_n_rerank, self.index.ntotal)
        scores, indices = self.index.search(query_fused_vec, search_k)

        candidates = []
        for base_score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            item = self.metadata[idx]
            ingredient_score = ingredient_similarity_from_vectors(
                query_ingredient_vecs,
                item.get("ingredient_vecs", []),
            )

            final_score = (W_BASE * float(base_score)) + (W_INGREDIENT * ingredient_score)

            candidates.append(
                {
                    "id": item["id"],
                    "image_path": item["image_path"],
                    "description": item.get("description", ""),
                    "ingredients": item.get("ingredients", []),
                    "base_score": round(float(base_score), 4),
                    "ingredient_score": round(float(ingredient_score), 4),
                    "score": round(float(final_score), 4),
                }
            )

        candidates.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query_description": query_description,
            "query_ingredients": query_ingredients,
            "top_k": candidates[:top_k],
        }