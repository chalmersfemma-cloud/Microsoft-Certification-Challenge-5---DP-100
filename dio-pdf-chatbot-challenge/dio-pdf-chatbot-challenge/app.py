from __future__ import annotations

import shutil
from pathlib import Path

import streamlit as st

from src.config import settings
from src.rag import RAGService


st.set_page_config(page_title=settings.app_title, page_icon="📄", layout="wide")
service = RAGService()


def copy_bundled_pdfs(destination: Path) -> int:
    bundled_dir = Path("sample_pdfs")
    count = 0
    for pdf_file in bundled_dir.glob("*.pdf"):
        shutil.copy2(pdf_file, destination / pdf_file.name)
        count += 1
    return count


def save_uploaded_files(uploaded_files, destination: Path) -> int:
    count = 0
    for uploaded_file in uploaded_files:
        target_path = destination / uploaded_file.name
        target_path.write_bytes(uploaded_file.getbuffer())
        count += 1
    return count


st.title(settings.app_title)
st.caption(
    "Interactive PDF chatbot with embeddings, vector search, and grounded answers."
)

with st.sidebar:
    st.header("Configuration")
    st.write(f"Embedding mode: **{service.embeddings.mode}**")
    st.write(f"Answer mode: **{service.llm.mode}**")
    st.write(f"Azure configured: **{'Yes' if settings.is_azure_configured else 'No'}**")
    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Use bundled sample PDFs", use_container_width=True):
        copied = copy_bundled_pdfs(settings.pdf_dir)
        st.success(f"Copied {copied} bundled PDFs into {settings.pdf_dir}")

    if uploaded_files and st.button("Save uploaded PDFs", use_container_width=True):
        saved = save_uploaded_files(uploaded_files, settings.pdf_dir)
        st.success(f"Saved {saved} PDFs to {settings.pdf_dir}")

    if st.button("Build / rebuild index", use_container_width=True):
        with st.spinner("Indexing PDFs..."):
            stats = service.ingest_directory(settings.pdf_dir, clear=True)
        st.success(
            f"Indexed {stats['pdf_count']} PDFs, {stats['page_count']} pages, and {stats['chunk_count']} chunks."
        )
        st.json(stats)

st.subheader("Indexed PDF folder")
st.code(str(settings.pdf_dir))
current_pdfs = sorted(path.name for path in settings.pdf_dir.glob("*.pdf"))
if current_pdfs:
    st.write("Loaded PDF files:")
    st.write("\n".join(f"- {name}" for name in current_pdfs))
else:
    st.info(
        "No PDFs saved yet. Use the sidebar to copy the bundled samples or upload your own files."
    )

st.divider()
st.subheader("Ask questions about the indexed PDFs")
question = st.text_input(
    "Question", placeholder="What are the main governance recommendations?"
)

if st.button("Ask", type="primary"):
    if not service.store.exists():
        st.warning("No vector index found yet. Save PDFs and build the index first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = service.ask(question)
        st.markdown("### Answer")
        st.write(result.answer)
        st.markdown("### Sources")
        for rank, (chunk, score) in enumerate(result.sources, start=1):
            with st.expander(
                f"Source {rank} - {chunk.source_file} - page {chunk.page_number} - score {score:.4f}"
            ):
                st.write(chunk.text)
