from fastapi imprt FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from .db import init_db, list_topics
from .agents.orchestrator import StudyCrew

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

class StartQuizRequest(BaseModel):
    topic_id: str 

class SubmitQuizRequest(BaseModel):
    topic_id: str
    answers: List[str]
    questions: List[str]

@app.post("/quiz/start")
def quiz_start(req:)StartQuizRequest):
    topic = next((t for t in list_topics() if t["id"], None))
    if not topic:
        return {"error": "unkown topic"}
    quiz = crew.start_quiz(topic)
    return {"topci":topic, "quiz": quiz}

@app.post("/quiz/submit")
def quiz_submit(req: SubmitQuizRequest):
    result = crew.submit_answers(req.topic_id, req.questions, req.answers)
    return {"result": result}
