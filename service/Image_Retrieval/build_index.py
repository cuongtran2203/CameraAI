import json
from pathlib import Path

import faiss
import numpy as np
from PIL import Image

from utils import encode_image, encode_text, fuse_features, call_vlm_vision


def build_index(image_dir: str, output_index: str, output_metadata: str):
    image_dir = Path(image_dir)

    if not image_dir.exists():
        raise RuntimeError(f"Image directory does not exist: {image_dir}")

    Path(output_index).parent.mkdir(parents=True, exist_ok=True)
    Path(output_metadata).parent.mkdir(parents=True, exist_ok=True)

    items = []
    vectors = []

    image_files = (
        list(image_dir.glob("*.jpg"))
        + list(image_dir.glob("*.png"))
        + list(image_dir.glob("*.jpeg"))
    )

    if not image_files:
        raise RuntimeError(f"No images found in {image_dir}")

    for i, path in enumerate(image_files):
        image = Image.open(path).convert("RGB")

        image_vec = encode_image(image)

        vlm_result = call_vlm_vision(image)
        dense_caption = vlm_result["dense_caption"]
        ingredients = vlm_result["ingredients"]

        dense_vec = encode_text(dense_caption)
        sparse_vec = encode_text(", ".join(ingredients))

        fused_vec = fuse_features(image_vec, dense_vec, sparse_vec).astype("float32")
        vectors.append(fused_vec)

        items.append({
            "id": f"item_{i:06d}",
            "image_path": str(path),
            "description": dense_caption,
            "ingredients": ingredients,
        })

        print(f"Indexed: {path.name}")

    mat = np.stack(vectors).astype("float32")
    faiss.normalize_L2(mat)

    index = faiss.IndexFlatIP(mat.shape[1])
    index.add(mat)

    faiss.write_index(index, output_index)

    with open(output_metadata, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"Saved FAISS index to: {output_index}")
    print(f"Saved metadata to: {output_metadata}")
    print(f"Total indexed images: {len(items)}")


if __name__ == "__main__":
    build_index(
        image_dir="images",
        output_index="data/faiss.index",
        output_metadata="data/metadata.json",
    )