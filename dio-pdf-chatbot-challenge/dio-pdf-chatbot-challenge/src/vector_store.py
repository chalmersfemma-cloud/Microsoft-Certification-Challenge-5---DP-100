from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.schemas import DocumentChunk


class LocalVectorStore:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.base_dir / "index.faiss"
        self.embeddings_path = self.base_dir / "embeddings.npy"
        self.metadata_path = self.base_dir / "chunks.json"

    def clear(self) -> None:
        for path in [self.index_path, self.embeddings_path, self.metadata_path]:
            if path.exists():
                path.unlink()

    def save(self, embeddings: np.ndarray, chunks: list[DocumentChunk]) -> None:
        if embeddings.size == 0:
            raise ValueError("Cannot save an empty embedding matrix")

        normalized = embeddings.astype("float32")
        norms = np.linalg.norm(normalized, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized = normalized / norms

        np.save(self.embeddings_path, normalized)
        self.metadata_path.write_text(
            json.dumps([chunk.to_dict() for chunk in chunks], indent=2),
            encoding="utf-8",
        )

        try:
            import faiss

            index = faiss.IndexFlatIP(normalized.shape[1])
            index.add(normalized)
            faiss.write_index(index, str(self.index_path))
        except Exception:
            pass

    def exists(self) -> bool:
        return self.embeddings_path.exists() and self.metadata_path.exists()

    def load(self) -> tuple[np.ndarray, list[DocumentChunk]]:
        if not self.exists():
            raise FileNotFoundError("Vector index not found. Run ingestion first.")
        embeddings = np.load(self.embeddings_path).astype("float32")
        chunks = [
            DocumentChunk.from_dict(item)
            for item in json.loads(self.metadata_path.read_text(encoding="utf-8"))
        ]
        return embeddings, chunks

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> list[tuple[DocumentChunk, float]]:
        embeddings, chunks = self.load()
        query = query_vector.astype("float32")
        query = query / max(np.linalg.norm(query), 1e-12)

        if self.index_path.exists():
            try:
                import faiss

                index = faiss.read_index(str(self.index_path))
                scores, ids = index.search(np.expand_dims(query, axis=0), top_k)
                results = []
                for idx, score in zip(ids[0], scores[0]):
                    if idx == -1:
                        continue
                    results.append((chunks[int(idx)], float(score)))
                return results
            except Exception:
                pass

        scores = embeddings @ query
        best_ids = np.argsort(scores)[::-1][:top_k]
        return [(chunks[int(idx)], float(scores[int(idx)])) for idx in best_ids]
