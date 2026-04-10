from fastapi import APIRouter, HTTPException
import json

from backend.app.models.responses import AnalyzeResponse, QASource
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.llm_service import LLMService
from backend.app.services.vector_service import VectorService

router = APIRouter()


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

        context = "\n\n".join(chunk["text"][:500] for chunk in chunks[:5])

        summary = LLMService.answer_question(
            question="Summarize this document in 5 to 8 concise bullet points.",
            context=context,
        )

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
            "confidential information definition",
            "term of agreement",
            "termination",
            "governing law",
            "third party disclosure",
            "return or destruction of confidential information",
            "exceptions to confidentiality",
        ]

        merged_results = []
        seen_chunk_ids = set()

        for query in retrieval_queries:
            query_embedding = EmbeddingService.embed_query(query)
            results = VectorService.search_document(
                document_id=document_id,
                query_embedding=query_embedding,
                top_k=3,
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

        context_parts = []
        sources = []

        for item in merged_results[:8]:
            chunk = item["chunk"]
            score = item["score"]

            context_parts.append(
                f"[Page {chunk['page_number']} | Score {score:.4f}]\n{chunk['text']}"
            )

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
