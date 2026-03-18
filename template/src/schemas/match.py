from pydantic import BaseModel
from typing import List, Optional

class MatchRequest(BaseModel):
    query_image_url: Optional[str] = None
    query_text: Optional[str] = None
    top_k: int = 5
    should_fuse: bool = True
    w_img: float = 0.5
    w_text: float = 0.5

class MatchResult(BaseModel):
    image_id: str
    score: float
    description: Optional[str] = None

class MatchResponse(BaseModel):
    results: List[MatchResult]
