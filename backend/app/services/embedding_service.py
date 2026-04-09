from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    @classmethod
    def embed_texts(cls, texts: List[str]) -> np.ndarray:
        model = cls.get_model()
        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.astype("float32")

    @classmethod
    def embed_query(cls, text: str) -> np.ndarray:
        model = cls.get_model()
        embedding = model.encode(
            [text],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embedding.astype("float32")
