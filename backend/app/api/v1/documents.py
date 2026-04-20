from fastapi import APIRouter
from pathlib import Path
import os

router = APIRouter()

UPLOAD_DIR = Path("/app/app/storage/uploads")


@router.get("/documents")
def list_documents():
    documents = []

    if not UPLOAD_DIR.exists():
        return {"documents": []}

    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            doc_id = file.name.split("_")[0]

            documents.append(
                {
                    "id": doc_id,
                    "name": file.name.split("_", 1)[-1],
                    "type": "Unknown",
                    "status": "Analysis Ready",
                    "updated_at": file.stat().st_mtime,
                }
            )

    return {"documents": documents}
