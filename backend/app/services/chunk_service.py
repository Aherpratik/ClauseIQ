from typing import List, Dict
import uuid


class ChunkService:
    @staticmethod
    def chunk_pages(
        document_id: str,
        pages: List[Dict],
        chunk_size: int = 700,
        overlap: int = 120,
    ) -> List[Dict]:
        chunks: List[Dict] = []

        for page in pages:
            page_number = page["page_number"]
            text = page["text"]

            if not text or not text.strip():
                continue

            page_chunks = ChunkService._chunk_single_page(
                document_id=document_id,
                page_number=page_number,
                text=text,
                chunk_size=chunk_size,
                overlap=overlap,
            )
            chunks.extend(page_chunks)
        return chunks

    @staticmethod
    def _chunk_single_page(
        document_id: str,
        page_number: int,
        text: str,
        chunk_size: int,
        overlap: int,
    ) -> List[Dict]:
        chunks: List[Dict] = []
        text_length = len(text)

        start = 0
        while start < text_length:
            target_end = min(start + chunk_size, text_length)
            end = ChunkService._find_good_breakpoint(text, start, target_end)

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": str(uuid.uuid4()),
                        "document_id": document_id,
                        "page_number": page_number,
                        "text": chunk_text,
                        "start_char": start,
                        "end_char": end,
                        "length": len(chunk_text),
                    }
                )

            if end >= text_length:
                break

            next_start = max(end - overlap, 0)

            if next_start <= start:
                break

            start = next_start

        return chunks

    @staticmethod
    def _find_good_breakpoint(text: str, start: int, target_end: int) -> int:
        if target_end >= len(text):
            return len(text)

        search_window = text[start:target_end]

        paragraph_break = search_window.rfind("\n\n")
        if paragraph_break != -1 and paragraph_break > int(len(search_window) * 0.6):
            return start + paragraph_break

        newline_break = search_window.rfind("\n")
        if newline_break != -1 and newline_break > int(len(search_window) * 0.6):
            return start + newline_break

        sentence_break = max(
            search_window.rfind(". "),
            search_window.rfind("? "),
            search_window.rfind("! "),
        )
        if sentence_break != -1 and sentence_break > int(len(search_window) * 0.6):
            return start + sentence_break + 1

        space_break = search_window.rfind(" ")
        if space_break != -1 and space_break > int(len(search_window) * 0.6):
            return start + space_break

        return target_end
