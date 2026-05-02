from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# Ensure `scripts/` is importable so we can `import graph` (scripts/graph.py)
SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

load_dotenv()

from graph import compiled_workflow  # noqa: E402


USECASES = {
    "Automated Clinical Trial Screening": (
        "Find candidates matching strict criteria. Example: 'Must have Asthma and be on Albuterol'."
    ),
    "Patient Handover / Transfer Summary": (
        "Generate a standardized transfer note from the most relevant encounter narrative."
    ),
    "Real-World Evidence (RWE) Mining": (
        "Turn unstructured notes into structured data you can analyze."
    ),
}


def _build_query(usecase: str, user_query: str) -> str:
    # Keep this minimal: just a prefix so the extractor knows the intent.
    return f"Use case: {usecase}. Query: {user_query}".strip()


def _run_pipeline(usecase: str, user_query: str) -> dict:
    inputs: dict = {
        "query": _build_query(usecase, user_query),
        "context": "",
        "structured_data": {},
        "metrics": {},
    }

    # Stream node-by-node and merge partial updates into a single state.
    final_state = dict(inputs)
    for step in compiled_workflow.stream(inputs):
        for _node_name, update in step.items():
            if isinstance(update, dict):
                final_state.update(update)

    return final_state


st.set_page_config(page_title="MedExtract", page_icon="🩺")
st.title("MedExtract")

usecase = st.selectbox("Use case", list(USECASES.keys()))
st.caption(USECASES[usecase])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your query (e.g., 'Must have Asthma and be on Albuterol')")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            with st.spinner("Running retrieval → extraction → grading..."):
                result = _run_pipeline(usecase, prompt)

            extracted = result.get("structured_data", {}) or {}
            metrics = result.get("metrics", {}) or {}

            st.subheader("Extracted JSON")
            st.json(extracted)

            st.subheader("Scores")
            col1, col2 = st.columns(2)
            col1.metric("Accuracy", metrics.get("accuracy", ""))
            col2.metric("Faithfulness", metrics.get("faithfulness", ""))

            summary = extracted.get("summary")
            if summary:
                st.markdown("**Summary**")
                st.write(summary)

            reasoning = metrics.get("reasoning")
            if reasoning:
                st.markdown("**Grader reasoning**")
                st.write(reasoning)

            # Keep the chat transcript lightweight.
            assistant_text = {
                "summary": summary,
                "accuracy": metrics.get("accuracy"),
                "faithfulness": metrics.get("faithfulness"),
            }
            st.session_state.messages.append(
                {"role": "assistant", "content": "```json\n" + json.dumps(assistant_text, indent=2) + "\n```"}
            )

        except Exception as e:
            st.error(
                "Pipeline failed. Common causes: missing OPENAI_API_KEY, missing PINECONE_* env vars, or an empty Pinecone index."  # noqa: E501
            )
            st.exception(e)
