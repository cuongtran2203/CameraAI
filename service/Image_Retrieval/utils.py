import base64
import io
import json
from typing import Any, Dict, List

import numpy as np
import torch
from fastapi import HTTPException
from PIL import Image

from config import W_DENSE, W_IMG, W_SPARSE
from model import DEVICE, VLM_MODEL, client, model, preprocess, tokenizer


def l2_normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


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


def load_image_from_path(path: str) -> Image.Image:
    try:
        return Image.open(path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Failed to load image from {path}: {str(e)}")


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


def normalize_ingredient(text: str) -> str:
    return " ".join(text.strip().lower().replace(".", "").split())


def encode_text_list(texts: List[str]) -> List[np.ndarray]:
    clean = [normalize_ingredient(t) for t in texts if t and t.strip()]
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


def parse_vlm_json(raw_text: str) -> Dict[str, Any]:
    raw_text = raw_text.strip()

    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw_text = "\n".join(lines).strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
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
            model=VLM_MODEL,
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

    data = parse_vlm_json(raw_text)

    dense_caption = str(data.get("dense_caption", "")).strip()
    ingredients = data.get("ingredients", [])
    if not isinstance(ingredients, list):
        ingredients = []

    ingredients = [normalize_ingredient(str(x)) for x in ingredients if str(x).strip()]

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
        "ingredient_vecs": ingredient_vecs,
        "fused_vec": fused_vec,
    }