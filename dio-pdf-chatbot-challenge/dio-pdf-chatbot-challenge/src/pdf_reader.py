from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pypdf import PdfReader



def extract_pages_from_pdf(pdf_path: Path) -> list[tuple[int, str]]:
    """Return a list of (page_number, text) tuples."""
    reader = PdfReader(str(pdf_path))
    pages: list[tuple[int, str]] = []

    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        normalized = " ".join(text.split())
        if normalized:
            pages.append((page_index, normalized))

    return pages



def discover_pdf_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.pdf") if path.is_file())



def iter_pdf_pages(pdf_files: Iterable[Path]) -> list[tuple[str, int, str]]:
    pages: list[tuple[str, int, str]] = []
    for pdf_file in pdf_files:
        for page_number, text in extract_pages_from_pdf(pdf_file):
            pages.append((pdf_file.name, page_number, text))
    return pages
