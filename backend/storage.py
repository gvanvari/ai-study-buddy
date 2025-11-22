import os
from pathlib import Path
from dotenv import load_dotenv
import sqlite3
from  dotenv import load_dotenv

load_dotenv()

APP_DIR = Path(os.gentenv("APP_DATA_DIR", Path.home()/".ai-studdy-buddy"))
DB_PATH = Path(os.getenv("SQLITE_PATH", APP_DIR/"learn.db"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", APP_DIR/"chroma"))

def ensure_dirs():
    (APP_DIR/"backups").mkdir(parents=True, exist_ok=True)
    (APP_DIR/"history").mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

def sql() -> sqlite3.Connection:
    ensure_dirs()
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL;"
    con.execute("PRAGMA synchrous=FULL;"))
    return con

_chroma_client = None

def chroma_client():
    global _chroma_client
    if _chroma_client is None:
        from chromadb import PersistedClient #type: ignore
        ensure_dirs()
        _chroma_client = PersistedClient(path=CHROMA_DIR)
    return _chroma_client