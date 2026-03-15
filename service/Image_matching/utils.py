import io
import json
import base64
from typing import Dict, Any

import faiss
import numpy as np
import torch
from PIL import Image
from fastapi import HTTPException

from model import model, preprocess, tokenizer, client, DEVICE, VLM_MODEL
from config import W_IMG, W_DENSE


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


def fuse_features(image_vec: np.ndarray, dense_vec: np.ndarray) -> np.ndarray:
    fused = (W_IMG * image_vec) + (W_DENSE * dense_vec)
    return l2_normalize(fused.astype(np.float32))


def call_vlm_caption(image: Image.Image) -> Dict[str, Any]:
    image_url = pil_to_data_url(image)

    prompt = """
        You are analyzing a food image for fine-grained image matching.

        Return ONLY valid JSON with this exact schema:
        {
        "dense_caption": "one detailed sentence describing the dish, cooking style, visible ingredients, side items, sauces, and plating"
        }

        Rules:
        - Focus only on visible food.
        - No markdown.
        - No extra keys.
        - No explanation outside JSON.
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

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Model did not return valid JSON: {raw_text}"
        )

    dense_caption = str(data.get("dense_caption", "")).strip()

    return {
        "dense_caption": dense_caption
    }

import time
def analyze_food_image(image: Image.Image) -> Dict[str, Any]:
    # Input byte 64 is to much to process (fix later)
    # start_time = time.time()
    vlm_result = call_vlm_caption(image)
    # end_time = time.time()
    # print(f"VLM captioning time: {end_time - start_time:.2f} seconds")

    dense_caption = vlm_result["dense_caption"]

    image_vec = encode_image(image)
    dense_vec = encode_text(dense_caption)

    fused_vec = fuse_features(image_vec, dense_vec)

    return {
        "dense_caption": dense_caption,
        "image_vec": image_vec,
        "dense_vec": dense_vec,
        "fused_vec": fused_vec,
    }