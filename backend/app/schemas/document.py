from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

class DocumentResponse(BaseModel):
    document_id: Annotated[str, Field(..., description='ID of the Document', examples=['P001'])]
    filename: Annotated[str, Field(..., description='File/document Name', examples=['abc.pdf'])]
    status: Annotated[str, Field(..., description='Document Processed or NOT', examples=['not_processed'])]