from pathlib import Path

import numpy as np

from src.schemas import DocumentChunk
from src.vector_store import LocalVectorStore


def test_vector_store_round_trip(tmp_path: Path) -> None:
    store = LocalVectorStore(tmp_path)
    chunks = [
        DocumentChunk("chunk-1", "a.pdf", 1, "player tracking data"),
        DocumentChunk("chunk-2", "b.pdf", 2, "injury prevention workload"),
    ]
    embeddings = np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype="float32")
    store.save(embeddings, chunks)

    results = store.search(np.asarray([1.0, 0.0], dtype="float32"), top_k=1)
    assert len(results) == 1
    assert results[0][0].source_file == "a.pdf"
