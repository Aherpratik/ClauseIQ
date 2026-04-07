from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from backend.app.models.responses import (
    UploadedDocumentResponse,
    ExtractedDocumentResponse,
)
from backend.app.services.pdf_services import PDFService

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

        return ExtractedDocumentResponse(
            document_id=document_id,
            filename=extracted["filename"],
            total_pages=extracted["total_pages"],
            full_text=extracted["full_text"],
            pages=extracted["pages"],
            metadata=extracted["metadata"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction Failed: {str(e)}")
