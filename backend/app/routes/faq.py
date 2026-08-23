# app/routes/faq.py

from fastapi import APIRouter, HTTPException

from app.services.faq_service import generate_pdf_faqs


router = APIRouter(
    prefix="/faq",
    tags=["FAQ"],
)


@router.get("/{document_id}")
def get_document_faqs(document_id: str):

    try:
        faqs = generate_pdf_faqs(document_id)

        return faqs

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate FAQs.",
        )