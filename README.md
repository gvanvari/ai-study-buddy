# AI Study Buddy (Local, Mac-friendly)

A local, personal learning assistant for AppSec, DSA and System Design

It stores your progress in **SQLite**, keeps semantic notes in **ChromaDB**, and shows a simple **StreamLit UI**

This template is the smallest possible **working** version:

- FastAPI backend with health + topics endpoints
- SQLite DB initialization & sample topics
- Streamlit UI showing topics and simple due list

---

## Prereqs

1. homebrew
2. python 3.12
3. pipenv

## Setup

From this folder:

```
pipenv install --dev
piepnv run python -m install torch
mkdir -p ~/.ai-study-buddy
cp .env.example .env
```

`PIPENV_PYTHON =$(which python3.12) pipenv install --dev`

## Run it

pipenv run ui (http://127.0.0.1:8501)
pipenv run ingest
pipenv run api (http://127.0.0.1:8000/health)

## Folder layout

```
ai-studdy-buddy/
    backend/
        api.py
        db.py
        storage.py
        agents/
    frontend/
        app.py
    tools/
        ingetst.py
    Pipfile
    .env.example
    README.md
```

pip install --user pipenv
