from fastapi import APIRouter

from app.services.pyq_service import analyze_pyq
from app.schemas.pyq import PYQAnalysis


router = APIRouter(
    prefix="/pyq",
    tags=["PYQ Intelligence"]
)


@router.get(
    "/{document_id}/analysis",
    response_model=PYQAnalysis
)
def get_pyq_analysis(document_id: str):

    return analyze_pyq(document_id)