from fastapi import APIRouter, Depends, HTTPException
from schemas.match import MatchRequest, MatchResponse
from services.matcher import MatcherService

router = APIRouter()

def get_matcher_service():
    return MatcherService()

@router.post("/", response_model=MatchResponse)
async def match_image_text(
    request: MatchRequest,
    matcher: MatcherService = Depends(get_matcher_service)
):
    try:
        results = await matcher.find_matches(request)
        return MatchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
