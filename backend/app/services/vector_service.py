from pathlib import Path
from typing import List, Dict
import json
import faiss  # type: ignore
import numpy as np


class VectorService:
    INDEX_DIR = Path("/app/app/storage/indexes")
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _index_path(cls, document_id: str) -> Path:
        return cls.INDEX_DIR / f"{document_id}.index"

    @classmethod
    def _metadata_path(cls, document_id: str) -> Path:
        return cls.INDEX_DIR / f"{document_id}_chunks.json"

    @classmethod
    def save_document_index(
        cls,
        document_id: str,
        embeddings: np.ndarray,
        chunks: List[Dict],
    ) -> Dict:
        if len(embeddings) == 0:
            raise ValueError("No embeddings to index.")

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        index_path = cls._index_path(document_id)
        metadata_path = cls._metadata_path(document_id)

        print("SAVE index path:", index_path.resolve())
        print("SAVE metadata path:", metadata_path.resolve())

        faiss.write_index(index, str(index_path))

        with metadata_path.open("w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        print("SAVE metadata exists after write:", metadata_path.exists())

        return {
            "document_id": document_id,
            "num_chunks": len(chunks),
            "embedding_dimension": dimension,
            "index_path": str(index_path),
            "metadata_path": str(metadata_path),
        }

    @classmethod
    def search_document(
        cls,
        document_id: str,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> List[Dict]:
        index_path = cls._index_path(document_id)
        metadata_path = cls._metadata_path(document_id)

        print("SEARCH index path:", index_path.resolve())
        print("SEARCH metadata path:", metadata_path.resolve())
        print("SEARCH index exists:", index_path.exists())
        print("SEARCH metadata exists:", metadata_path.exists())

        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("Index or metadata not found for document.")

        index = faiss.read_index(str(index_path))

        with metadata_path.open("r", encoding="utf-8") as f:
            chunks = json.load(f)

        scores, indices = index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = chunks[idx]
            results.append(
                {
                    "score": float(score),
                    "chunk": chunk,
                }
            )

        return results
