from fastapi import APIRouter, UploadFile, File
import os
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = "backend/app/storage/uploads"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename, "status": "uploaded"}
