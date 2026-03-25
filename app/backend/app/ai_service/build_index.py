import json
import time
from pathlib import Path
from typing import List
import os
import faiss
import numpy as np
from PIL import Image

from utils import analyze_food_image


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def list_image_files(image_dir: Path) -> List[Path]:
    files = [p for p in image_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    return sorted(files)


def build_index(image_dir: str, output_index: str, output_metadata: str) -> None:
    image_dir_path = Path(image_dir)
    output_index_path = Path(output_index)
    output_metadata_path = Path(output_metadata)

    if not image_dir_path.exists():
        raise RuntimeError(f"Image directory does not exist: {image_dir_path}")

    image_files = list_image_files(image_dir_path)
    if not image_files:
        raise RuntimeError(f"No supported images found in: {image_dir_path}")

    output_index_path.parent.mkdir(parents=True, exist_ok=True)
    output_metadata_path.parent.mkdir(parents=True, exist_ok=True)

    metadata = []
    fused_vectors = []

    total_start = time.perf_counter()

    for idx, image_path in enumerate(image_files):
        item_start = time.perf_counter()

        try:
            image = Image.open(image_path).convert("RGB")
            result = analyze_food_image(image)

            fused_vec = result["fused_vec"].astype("float32")
            ingredient_vecs = [
                vec.astype("float32").tolist() for vec in result["ingredient_vecs"]
            ]

            fused_vectors.append(fused_vec)
            file_name = os.path.basename(image_path)
            metadata.append(
                {
                    "id": file_name,
                    "image_path": str(image_path),
                    "description": result["dense_caption"],
                    "ingredients": result["ingredients"],
                    "ingredient_vecs": ingredient_vecs,
                }
            )

            item_time = time.perf_counter() - item_start
            print(f"[{idx + 1}/{len(image_files)}] {image_path.name} | total={item_time:.2f}s")

        except Exception as exc:
            print(f"[WARN] Failed to process {image_path.name}: {exc}")

    if not fused_vectors:
        raise RuntimeError("No images were successfully indexed.")

    matrix = np.stack(fused_vectors).astype("float32")
    faiss.normalize_L2(matrix)

    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(matrix)

    faiss.write_index(index, str(output_index_path))

    with output_metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    total_time = time.perf_counter() - total_start
    print(f"\nSaved index: {output_index_path}")
    print(f"Saved metadata: {output_metadata_path}")
    print(f"Indexed items: {len(metadata)}")
    print(f"Total build time: {total_time:.2f}s")


if __name__ == "__main__":
    build_index(
        image_dir="images",
        output_index="data/faiss.index",
        output_metadata="data/metadata.json",
    )