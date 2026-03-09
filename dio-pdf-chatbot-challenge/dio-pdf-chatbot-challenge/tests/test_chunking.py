from src.chunking import split_text


def test_split_text_returns_multiple_chunks_for_long_input() -> None:
    text = " ".join(["football"] * 400)
    chunks = split_text(text, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)


def test_split_text_rejects_invalid_overlap() -> None:
    try:
        split_text("hello world", chunk_size=50, overlap=50)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid overlap")
