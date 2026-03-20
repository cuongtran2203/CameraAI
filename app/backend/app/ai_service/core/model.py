import os
from pathlib import Path

import open_clip
import torch
from openai import OpenAI


def _load_dotenv(dotenv_path: str | Path = ".env") -> None:
    path = Path(dotenv_path)
    if not path.is_file():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = val


# Load environment variables from `.env` located in the `src/` package root.
# This keeps all runtime configuration within the source tree.
_load_dotenv("/home/app/Config/.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VLM_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", VLM_MODEL)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k",
    device=DEVICE,
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()
