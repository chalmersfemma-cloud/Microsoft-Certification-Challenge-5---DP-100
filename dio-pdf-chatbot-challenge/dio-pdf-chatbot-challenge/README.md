# DIO DP-100 Challenge - PDF Content Chatbot

A complete, GitHub-ready implementation of the DIO challenge **"Criando um Chatbot Baseado em Conteúdo de PDFs"** from **Microsoft Certification Challenge #5 - DP-100**.

This repository contains everything needed to demonstrate the challenge end-to-end:

- ingestion of multiple PDF files
- text extraction and chunking
- embedding generation
- vector search over PDF content
- grounded question answering with citations
- Streamlit chat interface
- local fallback mode for development
- Azure OpenAI-ready configuration for the original Azure-oriented workflow
- sample PDFs so the repository works immediately after cloning

## What this project does

The application lets you upload PDF files, build a searchable knowledge base, and ask questions grounded in the indexed document content.

### Core flow

1. Load one or more PDFs
2. Extract text page by page
3. Split the text into chunks
4. Generate embeddings for each chunk
5. Store embeddings in a local vector index
6. Retrieve the most relevant chunks for a question
7. Generate a grounded answer using Azure OpenAI when configured
8. Show citations and retrieved evidence in the UI

## Challenge alignment

This repo is designed to match the common structure used in public DIO challenge submissions:

- multiple PDFs are uploaded or stored in a project folder
- embeddings are created from document chunks
- vector similarity retrieval is used before answering
- an LLM produces grounded responses
- the app can be presented as a simple interactive chatbot UI

## Repository structure

```text
.
├── .env.example
├── .github/workflows/ci.yml
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── app.py
├── data
│   ├── index
│   └── uploads
├── docs
│   ├── architecture.md
│   ├── challenge-walkthrough.md
│   └── github-upload-checklist.md
├── sample_pdfs
│   ├── 01_ai_in_football_scouting.pdf
│   ├── 02_match_analysis_with_computer_vision.pdf
│   ├── 03_predictive_models_for_injury_prevention.pdf
│   └── 04_responsible_ai_in_sports.pdf
├── scripts
│   ├── chat_cli.py
│   ├── create_sample_pdfs.py
│   └── ingest.py
├── src
│   ├── __init__.py
│   ├── chunking.py
│   ├── config.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── pdf_reader.py
│   ├── prompts.py
│   ├── rag.py
│   ├── schemas.py
│   └── vector_store.py
└── tests
    ├── test_chunking.py
    └── test_vector_store.py
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

For the original challenge experience, fill in your Azure OpenAI settings in `.env`.

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Load PDFs

You can either:

- click **Use bundled sample PDFs**, or
- upload your own PDFs through the Streamlit sidebar

### 6. Build the index and chat

After indexing completes, ask questions such as:

- Which PDFs discuss risk reduction for athletes?
- How is computer vision applied to match analysis?
- What governance practices are recommended for responsible AI in sports?
- Which document talks about bias in scouting models?

## Local mode vs Azure mode

### Azure mode

When the Azure environment variables are present, the app will:

- use Azure OpenAI embeddings for document and query vectors
- use Azure OpenAI chat completions to generate the final answer

### Local mode

If Azure credentials are not configured, the app still works:

- embeddings are generated with `sentence-transformers`
- vector retrieval still works
- answers are produced in a grounded fallback format using the retrieved chunks

This makes the repository easy to review on GitHub even without a live Azure subscription.

## CLI usage

Build an index from the command line:

```bash
python scripts/ingest.py --input-dir sample_pdfs --clear
```

Run a terminal chat session:

```bash
python scripts/chat_cli.py
```

## Docker

```bash
docker build -t dio-pdf-chatbot .
docker run --rm -p 8501:8501 --env-file .env dio-pdf-chatbot
```

## Recommended GitHub steps

1. Create a new repository on GitHub
2. Upload all files from this project
3. Add screenshots after running the app locally
4. Replace sample PDFs with your own challenge theme if needed
5. Add a short section describing your learning outcomes

A detailed checklist is available in `docs/github-upload-checklist.md`.

## Suggested screenshots for the final GitHub submission

- Streamlit home screen
- PDF upload area
- successful indexing message
- sample questions and answers
- citations shown under the final answer

## Notes

- The included PDFs are original sample materials created for demonstration so the repository is immediately runnable.
- The code is intentionally modular to make the RAG pipeline easy to explain during the challenge review.
- The project is safe to publish because secrets are excluded and only `.env.example` is versioned.
