from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from backend.app.models.responses import (
    UploadedDocumentResponse,
    ExtractedDocumentResponse,
)
from backend.app.services.pdf_services import PDFService
from backend.app.services.chunk_service import ChunkService
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_service import VectorService


router = APIRouter()

UPLOAD_DIR = Path("backend/app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=UploadedDocumentResponse)
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Only PDF files are supported as of now."
        )

    document_id = str(uuid.uuid4())
    saved_filename = f"{document_id}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename

    try:
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        size_bytes = saved_path.stat().st_size

        return UploadedDocumentResponse(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            size_bytes=size_bytes,
            saved_path=str(saved_path),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File Uploaded failed : {str(e)}")


@router.get("/extract/{document_id}", response_model=ExtractedDocumentResponse)
def extract_document(document_id: str):
    matching_files = list(UPLOAD_DIR.glob(f"{document_id}_*.pdf"))

    if not matching_files:
        raise HTTPException(status_code=404, detail="Docuemnt Not Found. ")

    file_path = matching_files[0]

    try:
        extracted = PDFService.extract_text(str(file_path))

        chunks = ChunkService.chunk_pages(
            document_id=document_id,
            pages=extracted["pages"],
            chunk_size=700,
            overlap=120,
        )

        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = EmbeddingService.embed_texts(chunk_texts)

        VectorService.save_document_index(
            document_id=document_id,
            embeddings=embeddings,
            chunks=chunks,
        )

        return ExtractedDocumentResponse(
            document_id=document_id,
            filename=extracted["filename"],
            total_pages=extracted["total_pages"],
            full_text=extracted["full_text"],
            pages=extracted["pages"],
            metadata=extracted["metadata"],
            chunks=chunks,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction Failed: {str(e)}")


@router.get("/search/{document_id}")
def search_document(document_id: str, query: str, top_k: int = 5):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if top_k < 1 or top_k > 10:
        raise HTTPException(status_code=400, detail="Top_k must be between 1 and 10.")
    try:
        query_embedding = EmbeddingService.embed_query(query)
        results = VectorService.search_document(
            document_id=document_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )
        return {
            "document_id": document_id,
            "query": query,
            "top_k": top_k,
            "results": results,
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
