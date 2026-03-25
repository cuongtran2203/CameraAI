from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from api import router as api_router

app = FastAPI(title="Food Image Matching API")

# Add CORS middleware to allow the Vue frontend (Vite) to communicate with this AI service directly!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (localhost:5173, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

app.include_router(api_router)

images_dir = Path(__file__).resolve().parent / "images"
app.mount("/images", StaticFiles(directory=images_dir), name="images")