import io
import json
import base64
import re
from typing import Any, Dict, List

import faiss
import numpy as np
import torch
from fastapi import HTTPException
from PIL import Image

from core.config import W_DENSE, W_IMG, W_SPARSE
from core.model import (
    client,
    DEVICE,
    model,
    OPENAI_VISION_MODEL,
    preprocess,
    tokenizer,
)


def l2_normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


def faiss_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    a = vec_a.astype("float32").reshape(1, -1)
    b = vec_b.astype("float32").reshape(1, -1)

    faiss.normalize_L2(a)
    faiss.normalize_L2(b)

    index = faiss.IndexFlatIP(a.shape[1])
    index.add(b)
    scores, _ = index.search(a, k=1)

    return float(scores[0][0])


def pil_to_data_url(image: Image.Image, fmt: str = "JPEG") -> str:
    buffer = io.BytesIO()
    image.save(buffer, format=fmt)
    base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    mime = "image/jpeg" if fmt.upper() == "JPEG" else "image/png"
    return f"data:{mime};base64,{base64_str}"


def read_image(file_bytes: bytes) -> Image.Image:
    try:
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")


def encode_image(image: Image.Image) -> np.ndarray:
    image_tensor = preprocess(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    return image_features[0].detach().cpu().numpy().astype(np.float32)


def encode_text(text: str) -> np.ndarray:
    if not text.strip():
        return np.zeros((512,), dtype=np.float32)

    tokens = tokenizer([text]).to(DEVICE)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return text_features[0].detach().cpu().numpy().astype(np.float32)


def encode_text_list(texts: List[str]) -> List[np.ndarray]:
    clean = [t.strip().lower() for t in texts if t.strip()]
    if not clean:
        return []

    tokens = tokenizer(clean).to(DEVICE)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    return [feat.detach().cpu().numpy().astype(np.float32) for feat in text_features]


def fuse_features(
    image_vec: np.ndarray,
    dense_vec: np.ndarray,
    sparse_vec: np.ndarray,
) -> np.ndarray:
    fused = (W_IMG * image_vec) + (W_DENSE * dense_vec) + (W_SPARSE * sparse_vec)
    return l2_normalize(fused.astype(np.float32))


def ingredient_similarity(ingredients_a: List[str], ingredients_b: List[str]) -> float:
    if not ingredients_a or not ingredients_b:
        return 0.0

    emb_a = encode_text_list(ingredients_a)
    emb_b = encode_text_list(ingredients_b)

    if not emb_a or not emb_b:
        return 0.0

    mat_a = np.stack(emb_a).astype("float32")
    mat_b = np.stack(emb_b).astype("float32")

    faiss.normalize_L2(mat_a)
    faiss.normalize_L2(mat_b)

    index_b = faiss.IndexFlatIP(mat_b.shape[1])
    index_b.add(mat_b)
    scores_ab, _ = index_b.search(mat_a, 1)

    index_a = faiss.IndexFlatIP(mat_a.shape[1])
    index_a.add(mat_a)
    scores_ba, _ = index_a.search(mat_b, 1)

    return float((scores_ab.mean() + scores_ba.mean()) / 2.0)


def _strip_code_fences(text: str) -> str:
    text = text.strip()

    # Remove leading ```json or ``` fences
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def _extract_json_object(text: str) -> str:
    """Attempt to extract the first JSON object from text."""

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response")
    return match.group(0)


def parse_model_json(raw_text: str) -> Dict[str, Any]:
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=500, detail="Model returned empty response")

    cleaned = _strip_code_fences(raw_text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    try:
        json_text = _extract_json_object(cleaned)
        return json.loads(json_text)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Model did not return valid JSON: {raw_text}",
        )


def call_vlm_vision(image: Image.Image) -> Dict[str, Any]:
    image_url = pil_to_data_url(image)

    prompt = """
        You are an expert visual food analyst.

        Your task is to identify ONLY physically visible food components in the image.

        Return exactly one JSON object with this schema:
        {
        "dense_caption": "one detailed sentence describing the dish, cooking style, visible ingredients, sauces, and plating",
        "ingredients": ["visible ingredient 1", "visible ingredient 2", "visible ingredient 3"]
        }

        Rules:
        - Only list ingredients that are clearly visible.
        - Do not infer hidden seasonings, oil, sugar, salt, or sauces unless visible.
        - Use short noun phrases.
        - Output JSON only.
        - Do not wrap the response in markdown.
        - Do not use triple backticks.
    """

    try:
        response = client.chat.completions.create(
            model=OPENAI_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            temperature=0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VLM request failed: {str(e)}")

    try:
        raw_text = response.choices[0].message.content
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to parse model response")

    data = parse_model_json(raw_text)

    dense_caption = str(data.get("dense_caption", "")).strip()
    ingredients = data.get("ingredients", [])

    if not isinstance(ingredients, list):
        ingredients = []

    ingredients = [str(x).strip().lower() for x in ingredients if str(x).strip()]

    return {
        "dense_caption": dense_caption,
        "ingredients": ingredients,
    }


def analyze_food_image(image: Image.Image) -> Dict[str, Any]:
    vlm_result = call_vlm_vision(image)

    dense_caption = vlm_result["dense_caption"]
    ingredients = vlm_result["ingredients"]
    sparse_caption = ", ".join(ingredients)

    image_vec = encode_image(image)
    dense_vec = encode_text(dense_caption)
    sparse_vec = encode_text(sparse_caption)
    ingredient_vecs = encode_text_list(ingredients)

    fused_vec = fuse_features(image_vec, dense_vec, sparse_vec)

    return {
        "dense_caption": dense_caption,
        "ingredients": ingredients,
        "image_vec": image_vec,
        "dense_vec": dense_vec,
        "sparse_vec": sparse_vec,
        "fused_vec": fused_vec,
        "ingredient_vecs": ingredient_vecs,
    }
