from fastapi import APIRouter

from app.schemas.pyq import PYQAnalysis, PYQAnalysisRequest
from app.services.pyq_service import analyze_pyq


router = APIRouter(
    prefix="/api/pyq",
    tags=["PYQ Intelligence"],
)


@router.post(
    "/analyze",
    response_model=PYQAnalysis,
    summary="Analyze multiple previous-year question papers together",
)

def analyze_multiple_pyq_papers(request: PYQAnalysisRequest):
    return analyze_pyq(request)
