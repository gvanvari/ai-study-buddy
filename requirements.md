# Project goals

personal learning assistant - suggest daily study plans, review old topics, and introduce new ones intelligently
knowledge retention - use spaced repetition (SM-2 algo) so that you never forget older topics
active recall - auto generae quizzes, evaluate your answers
progress tracking - persist all your attempts, scores, and topics metadata for later review
visualization dashboard - show your current progress, weak areas, and inter topic dependencies in a knowledge graph view

## core feature

- each topic sored with domain, difficulty(1-3) , ease factor, interval, reps, dependencies

- quiz generation
  generate 3-5 MCQs, store generated questions locally for reuse
  use LLM through langchain/crewai to create these dynamically

- answer evaluation
  coach agent scores answer (0-10) and provides reasoning feedback
  updates spaced repetition factors (ease, interval, next review date).

- progress memory
  all progress saved in sqllite db
  daily automatic backup + optional markdown summary export

- visualization dashboard
  display- knowledge graph of all topics, node color=mastery, glow= due/overdue, click view details, recent attempts, start quiz button
  optional - domain coverage, weekly progress metrics,
 - local first architecture
   runs entirely on laptop

 - backup: Windows Task Scheduler + git (or a cross-platform backup script)

 - env: pipenv (or use `venv` + `pip` on Windows)

backend framework - fastapi - rest api for communication between dashboards and agents
frontend - streamlit - easy dashboard for skill graph and stats
graph redering - networkx+ pyvis or plotly - visualize knowledge graph interactively
database - sqllite
persistence utilities - sqlalchemy/sqlite-utils

## system architecture

streamlit UI -> FastAPI API (/topics,/quiz,/stats, connects to agents and db) -> agents

agents :
curriculum agent -> picks daily topics
quiz agent -> generates questions
coach agent -> evaluates answers
historian agent -> updates spaced repition

agents -> sqlit db(topics, attempts, questions)
