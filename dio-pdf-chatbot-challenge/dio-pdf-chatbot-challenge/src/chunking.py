from __future__ import annotations

from typing import Iterable

from src.schemas import DocumentChunk



def split_text(text: str, chunk_size: int = 900, overlap: int = 180) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        current_words = []
        current_len = 0
        end = start
        while end < len(words):
            next_word = words[end]
            extra = len(next_word) + (1 if current_words else 0)
            if current_len + extra > chunk_size and current_words:
                break
            current_words.append(next_word)
            current_len += extra
            end += 1
        chunks.append(" ".join(current_words))
        if end >= len(words):
            break
        overlap_words = []
        overlap_len = 0
        back = end - 1
        while back >= start:
            token = words[back]
            extra = len(token) + (1 if overlap_words else 0)
            if overlap_len + extra > overlap:
                break
            overlap_words.append(token)
            overlap_len += extra
            back -= 1
        start = max(back + 1, start + 1)
    return chunks



def build_chunks(
    page_rows: Iterable[tuple[str, int, str]],
    chunk_size: int = 900,
    overlap: int = 180,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    chunk_counter = 1

    for source_file, page_number, text in page_rows:
        for piece in split_text(text, chunk_size=chunk_size, overlap=overlap):
            chunks.append(
                DocumentChunk(
                    chunk_id=f"chunk-{chunk_counter:05d}",
                    source_file=source_file,
                    page_number=page_number,
                    text=piece,
                )
            )
            chunk_counter += 1

    return chunks
