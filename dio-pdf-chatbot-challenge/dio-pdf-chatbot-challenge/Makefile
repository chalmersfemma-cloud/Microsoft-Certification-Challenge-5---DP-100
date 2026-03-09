PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	streamlit run app.py

ingest:
	$(PYTHON) scripts/ingest.py --input-dir sample_pdfs --clear

test:
	pytest -q
