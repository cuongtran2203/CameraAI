"""
System Routes
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(prefix="/system", tags=["System"])


class StreamUrlResponse(BaseModel):
    mediamtx_hls_url: str   # HLS URL for browser (via MediaMTX)
    deepstream_rtsp_url: str  # Raw RTSP URL (DeepStream output)
    mediamtx_base: str      # Base URL of MediaMTX


@router.get("/stream-url", response_model=StreamUrlResponse)
async def get_stream_urls(
    current_user: User = Depends(get_current_user),
):
    """
    Returns all stream gateway URLs used by the frontend.

    - mediamtx_hls_url:  http://localhost:8888/{streamName}/hls.m3u8
                          Frontend encodes the user's RTSP URL as base64 to
                          form the streamName, so MediaMTX pulls it dynamically.
    - deepstream_rtsp_url: rtsp://mediamtx:8554/ds-test
                          The AI-processed stream (DeepStream YOLO output).
    - mediamtx_base: http://localhost:8888
    """
    return StreamUrlResponse(
        mediamtx_hls_url="http://localhost:8888/{streamName}/hls.m3u8",
        deepstream_rtsp_url="rtsp://mediamtx:8554/ds-test",
        mediamtx_base="http://localhost:8888",
    )
