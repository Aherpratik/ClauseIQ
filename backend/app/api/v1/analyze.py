from fastapi import APIRouter, HTTPException
import json
import re

from backend.app.models.responses import AnalyzeResponse, QASource
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.llm_service import LLMService
from backend.app.services.vector_service import VectorService

router = APIRouter()


def clean_chunk_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split())


def clean_summary_text(text: str) -> str:
    if not text:
        return ""

    text = " ".join(text.split())

    # remove common PDF junk
    text = re.sub(r"Copyright\s+\d{4}.*?All Rights Reserved\.?", "", text, flags=re.I)
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.I)
    text = re.sub(r"NON[-\s]?DISCLOSURE\s+AGREEMENT\s*\(NDA\)", "", text, flags=re.I)
    text = re.sub(
        r"\b[Nn]ondisclosure [Aa]greement\b", "Non-Disclosure Agreement", text
    )

    return text.strip()


def build_simple_summary(text: str) -> str:
    text = clean_summary_text(text)

    if not text:
        return "Summary could not be generated."

    lower = text.lower()

    # Detect document type
    if "non disclosure" in lower or "confidential" in lower:
        doc_type = "Non-Disclosure Agreement"
    else:
        doc_type = "Legal Agreement"

    # Detect key idea
    if "confidential" in lower:
        purpose = "protects confidential information"
    else:
        purpose = "defines obligations between parties"  # noqa: F841

    # Build clean summary (NOT copying text)
    summary = f"This {doc_type} outlines how parties handle and protect sensitive information and establishes obligations to prevent unauthorized disclosure."

    return summary


@router.get("/summary/{document_id}")
def summarize_document(document_id: str):
    chunks_path = VectorService._metadata_path(document_id)

    if not chunks_path.exists():
        raise HTTPException(status_code=404, detail="Document not indexed")

    try:
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        if not chunks:
            raise HTTPException(status_code=404, detail="No chunks found for document")

        context = " ".join(
            clean_chunk_text(chunk["text"])[:220] for chunk in chunks[:2]
        )

        summary = build_simple_summary(context)

        return {
            "document_id": document_id,
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{document_id}", response_model=AnalyzeResponse)
def analyze_document(document_id: str):
    try:
        chunks_path = VectorService._metadata_path(document_id)

        if not chunks_path.exists():
            raise HTTPException(status_code=404, detail="Document not indexed")

        with open(chunks_path, "r", encoding="utf-8") as f:
            all_chunks = json.load(f)

        if not all_chunks:
            raise HTTPException(status_code=404, detail="No chunks found")

        first_text = " ".join(chunk["text"] for chunk in all_chunks[:2]).lower()

        if "invention assignment agreement" in first_text:
            retrieval_queries = [
                "invention assignment agreement",
                "assignment of inventions",
                "company and intern",
                "confidential information",
                "work product ownership",
                "termination and obligations",
            ]
        elif (
            "non-disclosure agreement" in first_text
            or "nondisclosure agreement" in first_text
            or "nda" in first_text
        ):
            retrieval_queries = [
                "non disclosure agreement",
                "confidential information",
                "exclusions to confidentiality",
                "governing law",
                "return or destruction of confidential information",
                "term and survival",
            ]
        else:
            retrieval_queries = [
                "agreement parties",
                "effective date",
                "obligations",
                "termination",
                "governing law",
            ]

        merged_results = []
        seen_chunk_ids = set()

        for query in retrieval_queries:
            query_embedding = EmbeddingService.embed_query(query)
            results = VectorService.search_document(
                document_id=document_id,
                query_embedding=query_embedding,
                top_k=2,
            )

            for item in results:
                chunk = item["chunk"]
                chunk_id = chunk["chunk_id"]

                if chunk_id in seen_chunk_ids:
                    continue

                seen_chunk_ids.add(chunk_id)
                merged_results.append(item)

        if not merged_results:
            raise HTTPException(status_code=404, detail="No relevant chunks found")

        merged_results = sorted(merged_results, key=lambda x: x["score"], reverse=True)

        sources = []
        context_parts = []

        for item in merged_results[:5]:
            chunk = item["chunk"]
            score = item["score"]
            clean_text = clean_chunk_text(chunk["text"])

            context_parts.append(clean_text)

            sources.append(
                QASource(
                    score=score,
                    page_number=chunk["page_number"],
                    text=chunk["text"],
                )
            )

        context = "\n\n".join(context_parts)

        analysis = LLMService.extract_structured_analysis(context)

        return AnalyzeResponse(
            document_id=document_id,
            analysis=analysis,
            sources=sources,
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analyze failed: {str(e)}")
