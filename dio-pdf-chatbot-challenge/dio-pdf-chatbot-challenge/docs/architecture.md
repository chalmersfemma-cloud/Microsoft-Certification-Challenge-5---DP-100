# Architecture

## Components

### 1. Streamlit interface
Provides the user experience for:
- uploading PDF files
- copying bundled sample PDFs
- rebuilding the vector index
- asking questions
- reviewing retrieved source excerpts

### 2. PDF ingestion
The ingestion layer uses `pypdf` to extract text from each page and normalize whitespace.

### 3. Chunking
Each page is broken into overlapping chunks to preserve context while keeping retrieval efficient.

### 4. Embeddings
Two modes are supported:
- Azure OpenAI embeddings for the challenge-aligned cloud version
- SentenceTransformers for local development without cloud credentials

### 5. Vector search
A local vector store keeps embeddings plus chunk metadata. If `faiss` is available it is used for fast similarity search; otherwise the project falls back to NumPy cosine similarity.

### 6. Answer generation
When Azure is configured, the final answer is produced by an Azure OpenAI chat deployment and instructed to cite source blocks. Without Azure, the app returns a grounded fallback answer that still shows the best evidence.

## Data flow

```text
PDF files -> text extraction -> chunking -> embeddings -> vector index
question -> query embedding -> similarity search -> relevant chunks -> final answer
```

## Why this structure works well for the challenge

- easy to explain during presentation
- modular enough for future improvements
- grounded responses reduce hallucinations
- source citations make the output auditable
