import fitz
from pathlib import Path
from typing import Dict, List


class PDFService:
    @staticmethod
    def extract_text(file_path: str) -> Dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File Not Found: {file_path}")

        doc = fitz.open(file_path)

        pages: List[Dict] = []
        full_text_parts: List[str] = []

        for index, page in enumerate(doc):
            text = page.get_text("text")
            cleaned_text = PDFService._clean_text(text)

            pages.append({"page_number": index + 1, "text": cleaned_text})

            if cleaned_text.strip():
                full_text_parts.append(f"\n----Page {index + 1} -----\n{cleaned_text}")

        metadata = PDFService._extract_metadata(doc)

        result = {
            "filename": path.name,
            "total_pages": len(doc),
            "full_text": "\n".join(full_text_parts).strip(),
            "pages": pages,
            "metadata": metadata,
        }

        doc.close()

        return result

    @staticmethod
    def _clean_text(text: str) -> str:
        if not text:
            return ""

        lines = [line.strip() for line in text.splitlines()]
        not_empty_lines = [line for line in lines if line]
        return "\n".join(not_empty_lines)

    @staticmethod
    def _extract_metadata(doc) -> Dict[str, str]:
        raw_meta = doc.metadata or {}

        metadata = {
            "title": raw_meta.get("title", "") or "",
            "author": raw_meta.get("author", "") or "",
            "subject": raw_meta.get("subject", "") or "",
            "creator": raw_meta.get("creator", "") or "",
            "producer": raw_meta.get("producer", "") or "",
        }

        return metadata
