from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.chunking import build_chunks
from src.config import settings
from src.embeddings import EmbeddingProvider
from src.llm import AnswerGenerator
from src.pdf_reader import discover_pdf_files, iter_pdf_pages
from src.schemas import DocumentChunk
from src.vector_store import LocalVectorStore


@dataclass(slots=True)
class AnswerResult:
    answer: str
    sources: list[tuple[DocumentChunk, float]]


class RAGService:
    def __init__(self) -> None:
        self.embeddings = EmbeddingProvider()
        self.llm = AnswerGenerator()
        self.store = LocalVectorStore(settings.index_dir)

    def ingest_directory(self, input_dir: Path, clear: bool = False) -> dict[str, int | str]:
        if clear:
            self.store.clear()

        pdf_files = discover_pdf_files(input_dir)
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {input_dir}")

        page_rows = iter_pdf_pages(pdf_files)
        chunks = build_chunks(
            page_rows,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )
        embeddings = self.embeddings.embed_texts([chunk.text for chunk in chunks])
        self.store.save(embeddings, chunks)

        return {
            "pdf_count": len(pdf_files),
            "page_count": len(page_rows),
            "chunk_count": len(chunks),
            "embedding_mode": self.embeddings.mode,
        }

    def ask(self, question: str, top_k: int | None = None) -> AnswerResult:
        k = top_k or settings.top_k
        query_embedding = self.embeddings.embed_query(question)
        sources = self.store.search(query_embedding, top_k=k)
        answer = self.llm.generate(question, [chunk for chunk, _ in sources])
        return AnswerResult(answer=answer, sources=sources)
