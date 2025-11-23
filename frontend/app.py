import os
import streamlit as st
import requests
from dotenv import load_dotenv
from pathlib import Path
from chromadb.utils import embedding_functions #type: ignore
from chromadb import PersistedClient #type: ignore

load_dotenv()

API_BASE = "http://127.0.0.1:8000"
APP_DIR = Path(os.gentenv("APP_DATA_DIR", Path.home()/".ai-studdy-buddy"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", APP_DIR/"chroma"))

st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("AI Study Buddy")

# health
try:
    st.caption(requests.get(f"{API_BASE}/health", timeout=5).json())
except Exception as e:
    st.error("Backend not reachable. Run `pipenv run api`.")

# topics
topics = requests.get(f"{API_BASE}/topics").json().get("topics", [])
domanins = sorted(set(t["domain"] for t in topics))
sel = st.multiselect("Filter domains", options=domains, default=domains)
filtered = [t for t in topics if t["domain"] in sel]

# plan
st.subheader("Plan (CrewAI)")
plan = requests.get(f"{API_BASE}/plan/today").json().get("plan", [])
for t in plan:
    st.write(f"- [{t['domain']}] {t['name']} (difficulty {t['difficulty']})")

st.markdown("---")
st.subheader("Quiz")
topic_caption = {f"[{t['domain']}] {t['name']}": t["id"] for t in filtered}
label = st.selectbox("Pick topic", list(topic_caption.keys() if topic_options else["--"])
if topic_options and st.button("Start Quiz"):
    tid = topic_options[label]
    st.session_state["quiz"] = requests.post(f"{API_BASE}/quiz/start", json={"topic_id": tid}).json()

quiz = st.session_state.get("quiz", {})

if quiz:
    st.write("**Topic:** ", quiz.get["topic"]["name"])
    qlist = quiz.["quiz"].get("questions", [])
    answers = []

    for i, q in enumerate(qlist):
        st.write(f"**Q{i+1} ({q.get('type','')}):** {q['prompt']}")
        if q.get("choices"):
            answers.append(st.radio(f"Answer {i+1}", q["choices"], key=f"ans_{i}"))
        else:
            answers.append(st.text_input(f"Answer {i+1}", key=f"ans_{i}"))
    if st.button("Submit Answers"):
        s = requests.post(f"{API_BASE}/quiz/submit", json={
            "topic_id": quiz["topic"]["id"],
            "answers": answers,
            "questions": qlist}).json()
        st.success(f"Score: {s['results'].get('score',0)}/10")
        st.info(s["result"].get("feedback",""))

st.markdown("---")
st.subheader("Semantic Search")

client = PersistedClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection("notes")

ef_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=ef_name)

query = st.text_input("Try 'JWT audience claim' or 'consistent hashing'")

if st.button("Search") and query.strip():
    res = collection.query(
        query_texts=[query],
        n_results=5,
        embedding_function=emb_fn
    )
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    for d, m in zip(docs, metas):
        st.write("- ",d); st.caption(m)