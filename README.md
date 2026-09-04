# Board Game Rules Bot

A citation-backed Q&A bot for board game rulebooks. Upload a rulebook PDF,
ask it a rules question in plain English, and it answers using retrieved
sections of the actual rulebook, citing exactly where the answer came
from, and refusing to guess when a rule isn't covered.

Starting with *Root*'s Law of Root, built to extend to any rulebook via
game-tagged metadata.

## Why

Rules disputes in board games are common and rulebooks are often long and
cross-referential. Rather than a generic chatbot that might hallucinate a
plausible-sounding but wrong rule, this project is built around
retrieval-augmented generation (RAG): every answer is grounded in
retrieved text from the actual source document, with the section number
surfaced so it can be verified.

## How it works

1. **Ingest** — a rulebook PDF is parsed into text and split into chunks,
   keeping each chunk's section number attached.
2. **Embed** — each chunk is turned into a vector embedding and stored in
   Postgres via the `pgvector` extension.
3. **Retrieve** — a user's question is embedded the same way, and the
   database returns the most similar chunks by cosine distance.
4. **Guardrail** — if nothing retrieved is similar enough, the bot says
   the rule isn't covered instead of letting the model guess.
5. **Answer** — the retrieved chunks are passed to an LLM along with the
   question, with a prompt that forces citations and forbids answering
   outside the provided text.

## Tech stack

| Layer       | Choice                              |
|-------------|--------------------------------------|
| Backend     | FastAPI (Python)                     |
| Database    | PostgreSQL + `pgvector`              |
| Embeddings  | Voyage AI                            |
| LLM         | Claude (Anthropic API)               |
| Frontend    | React + Vite                         |
| Local dev   | Docker Compose                       |

## Project structure

_TBD as the project is built out._

## Getting started

_TBD — setup instructions will be added as the backend and frontend come
together._

## Roadmap

- [ ] Project skeleton (FastAPI app, Docker Compose, Postgres + pgvector)
- [ ] PDF ingestion + section-aware chunking
- [ ] Embedding pipeline
- [ ] Retrieval + guardrail
- [ ] LLM answer generation with citations
- [ ] Multi-game support
- [ ] React frontend
- [ ] Chat history persistence
- [ ] CI (GitHub Actions)
- [ ] AWS deployment
