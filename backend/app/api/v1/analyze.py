from fastapi import APIRouter, HTTPException
import json

from backend.app.models.responses import AnalyzeResponse, QASource
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.llm_service import LLMService
from backend.app.services.vector_service import VectorService

router = APIRouter()


def clean_chunk_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split())


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

        # keep summary context smaller and cleaner
        context = "\n\n".join(
            clean_chunk_text(chunk["text"])[:350] for chunk in chunks[:4]
        )

        summary = LLMService.summarize_document(context=context)

        return {
            "document_id": document_id,
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{document_id}", response_model=AnalyzeResponse)
def analyze_document(document_id: str):
    try:
        retrieval_queries = [
            "non disclosure agreement",
            "confidential information",
            "exclusions to confidentiality",
            "governing law",
            "return or destruction of confidential information",
            "term and survival",
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

        for item in merged_results[:6]:
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
