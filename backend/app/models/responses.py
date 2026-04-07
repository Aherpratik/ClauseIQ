from pydantic import BaseModel
from typing import List, Dict


class UploadedDocumentResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    saved_path: str


class PageText(BaseModel):
    page_number: int
    text: str


class ExtractedDocumentResponse(BaseModel):
    document_id: str
    filename: str
    total_pages: int
    full_text: str
    pages: List[PageText]
    metadata: Dict[str, str]
