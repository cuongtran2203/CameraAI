import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import faiss
import numpy as np
from fastapi import HTTPException

from core.config import (
    DEFAULT_TOP_K,
    TOP_N_RERANK,
    W_BASE,
    W_INGREDIENT,
)
from .vision import (
    call_vlm_vision,
    encode_image,
    encode_text,
    encode_text_list,
    fuse_features,
)


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
    def __init__(
        self,
        index_path: str,
        metadata_path: str,
    ):
        self.index_path = index_path
        self.metadata_path = metadata_path

        self.index = faiss.read_index(str(index_path))

        metadata_file = Path(metadata_path)
        if not metadata_file.exists():
            raise RuntimeError(f"Metadata file not found: {metadata_path}")

        with metadata_file.open("r", encoding="utf-8") as f:
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

        candidates: List[Dict[str, Any]] = []
        for base_score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            item = self.metadata[idx]
            ingredient_score = ingredient_similarity_from_vectors(
                query_ingredient_vecs,
                item.get("ingredient_vecs", []),
            )

            final_score = (W_BASE * float(base_score)) + (
                W_INGREDIENT * ingredient_score
            )

            base_dir = os.getenv("IMAGE_BASE_PATH", "/home/cuongtdm/Documents/tructt/service/CameraAI/app/backend/app/ai_service").rstrip("/")
            candidates.append(
                {
                    "id": item["id"],
                    "image_path": f"{base_dir}/{item['image_path']}",
                    "description": item.get("description", ""),
                    "ingredients": item.get("ingredients", []),
                    "base_score": round(float(base_score), 4),
                    "ingredient_score": round(float(ingredient_score), 4),
                    "score": round(float(final_score), 4),
                }
            )

        candidates.sort(key=lambda x: x["score"], reverse=True)

        # Only return the single best match if it meets the 0.75 threshold
        top_results = []
        if candidates and candidates[0]["score"] >= 0.75:
            top_results = [candidates[0]]

        return {
            "query_description": query_description,
            "query_ingredients": query_ingredients,
            "top_k": top_results[0],
        }


def get_default_retrieval_engine() -> FoodRetrievalEngine:
    """Create a retrieval engine using environment-default paths.

    The retrieval index and metadata paths can be overridden via env vars:
    - RETRIEVAL_INDEX_PATH
    - RETRIEVAL_METADATA_PATH
    """

    root = Path(__file__).resolve().parents[2]
    default_index = root / "Image_Retrieval" / "data" / "faiss.index"
    default_metadata = root / "Image_Retrieval" / "data" / "metadata.json"

    index_path = os.getenv("RETRIEVAL_INDEX_PATH", str(default_index))
    metadata_path = os.getenv("RETRIEVAL_METADATA_PATH", str(default_metadata))

    return FoodRetrievalEngine(
        index_path=index_path,
        metadata_path=metadata_path,
    )
