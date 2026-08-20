---
description: AI & LLM Architecture & RAG Pipeline Workflow
---

# 🤖 AI Engineering & RAG Pipeline Workflow

## Pre-conditions
- Model APIs configured in `.env` (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)
- Vector DB instance or embedded client configured

## Steps
1. **@speckit.ai-engineer** — Ingestion & Chunking Design
   - Define chunk size, overlap, metadata schema, and vector embedding model.
2. **@speckit.ai-engineer** — Hybrid Search & Retrieval
   - Implement dense vector search + BM25 keyword search + Reranking.
3. **@speckit.ai-engineer** — Strict Tool Calling & Structured Output
   - Define typed Pydantic / Zod schemas for all model outputs.
4. **@speckit.ai-engineer** — Automated Evaluation & Quality Gates
   - Run Ragas/TruLens evals on Golden Test Datasets (faithfulness, relevancy).
