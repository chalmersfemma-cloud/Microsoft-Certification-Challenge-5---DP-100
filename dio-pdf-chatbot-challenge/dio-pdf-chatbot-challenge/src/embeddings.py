from __future__ import annotations

from typing import Sequence

import numpy as np

from src.config import settings


class EmbeddingProvider:
    def __init__(self) -> None:
        self._mode = "azure" if settings.is_azure_configured else "local"
        self._local_model = None
        self._azure_client = None

    @property
    def mode(self) -> str:
        return self._mode

    def _get_local_model(self):
        if self._local_model is None:
            from sentence_transformers import SentenceTransformer

            self._local_model = SentenceTransformer(settings.local_embedding_model)
        return self._local_model

    def _get_azure_client(self):
        if self._azure_client is None:
            from openai import AzureOpenAI

            self._azure_client = AzureOpenAI(
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_endpoint=settings.azure_openai_endpoint,
            )
        return self._azure_client

    def embed_texts(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 0), dtype="float32")
        if self._mode == "azure":
            client = self._get_azure_client()
            response = client.embeddings.create(
                model=settings.azure_embedding_deployment,
                input=list(texts),
            )
            vectors = [item.embedding for item in response.data]
            return np.asarray(vectors, dtype="float32")

        model = self._get_local_model()
        vectors = model.encode(list(texts), normalize_embeddings=True)
        return np.asarray(vectors, dtype="float32")

    def embed_query(self, text: str) -> np.ndarray:
        query_vector = self.embed_texts([text])
        return query_vector[0]
