# Challenge Walkthrough

## Goal
Build a chatbot capable of answering questions based on the content of PDF files using embeddings, vector search, and generative AI.

## Step-by-step

### Step 1 - Prepare documents
Add PDF files to `sample_pdfs/` or upload them in the Streamlit interface.

### Step 2 - Build the index
Run the ingestion pipeline from the UI or with:

```bash
python scripts/ingest.py --input-dir sample_pdfs --clear
```

### Step 3 - Ask questions
Start the app:

```bash
streamlit run app.py
```

### Step 4 - Explain the pipeline in your GitHub submission
Mention these technical stages:
- PDF extraction
- chunking
- embeddings
- vector search
- grounded answering with citations

### Step 5 - Improve the project for your own submission
You can personalize the challenge by:
- replacing the sample PDFs with your own domain documents
- adding screenshots of the app
- switching local mode to full Azure mode
- documenting lessons learned in the README
