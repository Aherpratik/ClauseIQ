from pydantic import BaseModel
from typing import List, Dict, Any


class UploadedDocumentResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    saved_path: str


class PageText(BaseModel):
    page_number: int
    text: str


class ChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    text: str
    start_char: int
    end_char: int
    length: int


class ExtractedDocumentResponse(BaseModel):
    document_id: str
    filename: str
    total_pages: int
    full_text: str
    pages: List[PageText]
    metadata: Dict[str, str]
    chunks: List[ChunkResponse]


class IndexDocumentResponse(BaseModel):
    document_id: str
    num_chunks: int
    embedding_dimension: int
    index_path: str
    metadata_path: str


class SearchResultChunk(BaseModel):
    score: float
    chunk: ChunkResponse


class QARequest(BaseModel):
    question: str
    top_k: int = 5


class QASource(BaseModel):
    score: float
    page_number: int
    text: str


class QAResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    sources: List[QASource]


class AnalyzeResponse(BaseModel):
    document_id: str
    analysis: Dict[str, Any]
    sources: List[QASource]
