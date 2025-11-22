import os
import streamlit as st
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("AI Study Buddy")

#Sidebar
st.sidebar.header("Controls"
if st.sidebar.button("Refresh"):
    st.experimental_rerun()

try:
    response = requests.get(f"{API_BASE}/topics", timeout=5)
    response.raise_for_status()
    topics = response.json().get("topics", [])
except Exception as e:
    st.error(f"Could not reach the backend API: {e}")

domains = sorted(set(t["domain"] for t in topics))
selected = st.multiselect("Filter domains", options=domains, default=domains)

filtered = [t for t in topics if t["domain"] in selected]

st.subheder("Available Topics")
st.caption("Seeded with 3 sample items. You can add more later.")
for t in filtered:
    with st.expander(f"[{t['domain']}] {t{['name']}} - difficulty {t[difficulty]}");
        st.json(t)

st.markdown("---")
st.subheader("Semantic search demo")

from chromadb.utils import embedding_functions #type: ignore
from dotenv import load_dotenv
from chromadb import PersistedClient #type: ignore

APP_DIR = Path(os.gentenv("APP_DATA_DIR", Path.home()/".ai-studdy-buddy"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", APP_DIR/"chroma"))

client = PersistedClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection("notes")

ef_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=ef_name)

query = st.text_input("Type something like 'JWT audience claim' ")
ifs st.button("Search") and query.strip():
    try:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            embedding_function=emb_fn
        )
        st.write("Top matches:")
        for doc, meta in zip(results.get("documents", [])[0], results.get("metadatas", [])[0]):
            st.write("- ",doc)
            st.caption(meta)
    except Exception as e:
        st.error(f"Error during search: {e}")