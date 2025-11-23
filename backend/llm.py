import os
import langchain_openai import ChatOpenAI
from chromadb.utils import embedding_functions #type: ignore
from .storage import chroma_client

def get_chat_model():
    if os.getenv("OPENAI_API_KEY") :
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.2)
    raise RuntimeError("No OPENAI_API_KEY found in environment variables.")

def retrieve_contexxt(topic_id:str, query:str, k:int=5):
    client = chroma_client()
    coll = client.get_or_create_collection("notes")
    ef = embedding_functions.OpenAIEmbeddingFunction(model_name=os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2"))
    where = {"topic_id": topic_id} if topic_id else None
    res = coll.query(query_texts=[query or topic_id], n_results=k, where=where, embedding_function=ef)
    docs = (res.get("documents") or [[]])[0]
    return "\n".join(docs)
