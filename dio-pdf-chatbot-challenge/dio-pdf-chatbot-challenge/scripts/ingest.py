from __future__ import annotations

import argparse
from pathlib import Path

from src.rag import RAGService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the PDF chatbot index")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("sample_pdfs"),
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete any existing index before re-ingesting",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    service = RAGService()
    stats = service.ingest_directory(args.input_dir, clear=args.clear)
    print("Index built successfully")
    for key, value in stats.items():
        print(f"- {key}: {value}")
