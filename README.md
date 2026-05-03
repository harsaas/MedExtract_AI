# MedExtract AI

MedExtract AI is a minimal **clinical RAG + structured extraction** app that turns unstructured patient encounter narratives into **Pydantic-validated JSON**, and then **grades** the extraction (accuracy + faithfulness) to help you trust what you see.

- **Retrieval:** Pinecone (vector DB) via LlamaIndex retriever
- **Extraction:** OpenAI chat model with `with_structured_output()` into a Pydantic schema
- **Orchestration:** LangGraph (retrieve → extract → grade)
- **UI:** Streamlit chat interface

> This project is a demo/prototype for information extraction. It is **not medical advice** and is not a certified medical device. Avoid using PHI unless you have the right approvals and controls.

## Demo

Screenshots are in `screenshots/`.

## Quickstart (Windows / macOS / Linux)

### 1) Prerequisites

- Python **3.10+** (this repo was validated on Python 3.10)
- A Pinecone project + an index (serverless recommended)
- An OpenAI API key

### 2) Create a virtual environment + install dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file in the repo root:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medextract-index
PINECONE_INDEX_HOST=your_index_host
```

Notes:
- `PINECONE_INDEX_HOST` is shown in the Pinecone console for your index (it’s required by `scripts/retriever.py`).
- If you already have an index name/host, keep them as-is.

### 4) Upload sample narratives to Pinecone (one-time)

Put your clinical narratives under `data/processed_narratives/` and then run:

```bash
python scripts/upload_to_pinecone.py
```

This uses LlamaIndex to read documents and embed them during upload. If embedding fails, double-check `OPENAI_API_KEY`.

### 5) Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

In the UI:
- Select a use case (trial screening / handover summary / RWE mining)
- Ask a query like: `Must have Asthma and be on Albuterol`
- You’ll see:
  - **Extracted JSON** (`structured_data`)
  - **Scores** (accuracy + faithfulness)

## CLI runner (optional)

There’s also a simple CLI-style runner that streams node outputs:

```bash
python scripts/medextract_app/main.py
```

## How it works (high level)

1. **Retrieve**: `scripts/retriever.py` queries Pinecone via LlamaIndex and returns top-k chunks.
2. **Extract**: `scripts/pydantic_extractor.py` uses `ChatOpenAI(...).with_structured_output(PatientEncounter)`.
3. **Grade**: `scripts/llm_grader.py` uses a judge LLM with a `Metrics` schema.
4. **Orchestrate**: `scripts/graph.py` wires the nodes using LangGraph (`START → retrieve → extract → grade → END`).

## Repo structure

- `streamlit_app.py` — Streamlit chat UI
- `scripts/graph.py` — LangGraph workflow
- `scripts/retriever.py` — Pinecone-backed retriever (LlamaIndex)
- `scripts/pydantic_extractor.py` — Pydantic structured extraction
- `scripts/llm_grader.py` — LLM-based grading into metrics
- `scripts/pydantic_models/clinical.py` — `PatientEncounter` schema
- `scripts/pydantic_models/eval.py` — `Metrics` schema
- `scripts/upload_to_pinecone.py` — ingestion/upload utility

## Troubleshooting

### Streamlit warnings or no UI

Run Streamlit using:

```bash
streamlit run streamlit_app.py
```

(Do not run `python streamlit_app.py`.)

### Missing env vars

Common failures are missing:
- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_INDEX_HOST`

### Windows + OneDrive virtualenv issues

If your repo lives under OneDrive and `pip` starts failing with missing metadata/RECORD errors, move the repo to a non-synced folder (e.g., `C:\dev\...`) or recreate the virtual environment.

## Customization

- Model choice is currently hard-coded to `gpt-4o` in:
  - `scripts/pydantic_extractor.py`
  - `scripts/llm_grader.py`

If you want, we can switch to using an env var like `OPENAI_MODEL` for easier config.

---

If you build on this, consider adding: dataset versioning, redaction/PHI handling, prompt logging, and offline evals before production use.
