from fastapi imprt FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, list_topics

app = FastAPI(title ="AI Study Buddy API")

# allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501","http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/topics")
def topics()
    return {"topics": list_topics()}