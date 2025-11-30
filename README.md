# AI Study Buddy (Local, Windows 10)

A local, personal learning assistant for AppSec, DSA and System Design

It stores your progress in **SQLite**, keeps semantic notes in **ChromaDB**, and shows a simple **Streamlit UI**

This template is the smallest possible **working** version:

- FastAPI backend with health + topics endpoints
- SQLite DB initialization & sample topics
- Streamlit UI showing topics and simple due list

---

## Prereqs

1. Windows 10 (with PowerShell)
2. Python 3.12 (install from python.org or using `winget`/`chocolatey`)
3. `pipenv` (optional) or use a standard `venv` + `pip` workflow

## Setup (PowerShell)

From the project folder in PowerShell:

```powershell
# create a virtual environment (recommended)
python -m venv .venv
# activate (bash)
source venv/Scripts/activate
# or use pipenv if you prefer
pip install --upgrade pip
pip install pipenv
pipenv install --dev
# install optional heavy deps like torch (adjust for your GPU/CPU)
python -m pip install torch
# create app folder for local config
New-Item -ItemType Directory -Force $env:USERPROFILE\.ai-study-buddy
# copy environment example
Copy-Item .env.example .env
```

If using `pipenv` and you need to point it at a specific Python interpreter:

```powershell
#$env:PIPENV_PYTHON = 'C:\\Path\\To\\Python\\python.exe'
pipenv install --dev
```

## Run it

From an activated environment (PowerShell):

```powershell
# Streamlit UI
pipenv run ui    # or: streamlit run frontend/app.py --server.port 8501
# ingest data
pipenv run ingest
# start API
pipenv run api
# API health -> http://127.0.0.1:8000/health
```

## Folder layout

```
ai-study-buddy/
    backend/
        api.py
        db.py
        storage.py
        agents/
    frontend/
        app.py
    tools/
        ingest.py
    Pipfile
    .env.example
    README.md
```

## Architecture

```mermaid
flowchart LR
  %% Users & runtime
  User[User (browser / local user)]
  subgraph Runtime
    UIClient[Streamlit UI<br/>frontend/app.py]
    CLI[tools/ingest.py]
    Uvicorn[uvicorn (run backend.api)]
  end

  %% Backend components
  subgraph Backend
    API[FastAPI app<br/>backend/api.py]
    DB[SQLite DB<br/>backend/db.py]
    Storage[Local storage / file store<br/>backend/storage.py]
    Agents[Agents / Orchestrator<br/>backend/agents/orchestrator.py]
    Historian[HistorianAgent]
    Quiz[QuizAgent]
    Coach[CoachAgent]
    Curriculum[CurriculumAgent]
  end

  %% Vector DB / embeddings
  subgraph VectorStore
    Chroma[ChromaDB (vector DB)]
  end

  %% External / infra
  subgraph Infra
    Python[Python venv (.venv)]
    Requirements[requirements.txt / Pipfile]
  end

  %% Connections / flows
  User --> UIClient
  UIClient -->|HTTP (calls API endpoints)| API
  API --> Agents
  Agents -->|reads/writes| DB
  Agents -->|reads/writes| Chroma
  Agents --> Historian
  Agents --> Quiz
  Agents --> Coach
  Agents --> Curriculum
  CLI -->|ingest documents| Chroma
  CLI -->|create topics / metadata| DB
  Uvicorn --> API
  UIClient -->|local process| StreamlitConfig[/server: 127.0.0.1:8501/]
  API -->|health/topics endpoints| DB
  API -->|persist/serve| Storage

  %% notes
  note_right_of Chroma["Holds embeddings & semantic notes\nUsed by ingest & agents"]
  note_right_of DB["SQLite: topics, progress, history\nUsed by API & agents"]
  note_left_of Requirements["Dev + runtime packages\nfastapi, uvicorn, streamlit, chromadb, ..."]

  %% Agent interactions (detailed)
  Agents ---|orchestrates| Historian
  Agents ---|orchestrates| Quiz
  Agents ---|orchestrates| Coach
  Agents ---|orchestrates| Curriculum

  classDef service fill:#f9f,stroke:#333,stroke-width:1px;
  class API,Agents,Chroma,DB,UIClient,CLI service;
```