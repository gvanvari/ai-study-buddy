import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from chromadb import PersistedClient #type: ignore
from chromadb.utils import embedding_functions #type: ignore

APP_DIR = Path(os.gentenv("APP_DATA_DIR", Path.home()/".ai-studdy-buddy"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", APP_DIR/"chroma"))
client = PersistedClient(path=CHROMA_DIR)
notes = client.get_or_create_collection("notes")

docs = [(
    ("notes:jwt:001", "JWT audience must be validated for intended recipient", {"domain","topic_id":"appsec.jwt.aud-claim"}),
    ("notes:hash:001", "Consistent reduces remapping when nodes join/leave a cluster", {"domain","topic_id":"sd.constistent-hashing"}),
    ("notes:twosum2:001", "Two Sum II uses the sorted property of the array to use a two-pointer technique", {"domain","topic_id":"dsa.twoptr.167-two-sum-ii"}),
)]

ids, texts, metas = zip(*docs)
notes.upsert(ids=list(ids), documents=list(texts), metadatas=list(metas))

print(f"Ingested {len(docs)} documents into ChromaDB at {CHROMA_DIR}")