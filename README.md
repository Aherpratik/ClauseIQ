# ClauseIQ

ClauseIQ is a full-stack GenAI-powered document intelligence platform that enables users to upload documents, extract structured content, and generate actionable insights such as summaries, clauses, risks, and semantic search results.

---

##  Features

###  Document Processing
- Upload PDF documents via API or UI
- Extract structured, page-wise text using PyMuPDF
- Smart chunking with overlap for semantic understanding

###  AI-Powered Analysis
- Automatic document summarization
- Clause extraction and categorization
- Risk identification (high/medium insights)
- Key field detection from legal/business documents

###  Semantic Search
- Embedding-based retrieval using Sentence Transformers
- FAISS-powered vector search
- Relevant chunk retrieval for grounded answers

###  Ask AI (RAG-based QA)
- Context-aware question answering over documents
- Uses retrieved chunks for grounded responses
- Avoids hallucination with constrained prompting

###  Interactive Frontend (React + Tailwind)
- Workspace-style UI (like real SaaS product)
- Document viewer with page rendering
- Analysis panel with tabs:
  - Overview
  - Key Fields
  - Clauses
  - Risks
  - Ask AI
  - Search
- Real-time API integration (no mock data)

---

##  Architecture

```text
Upload → Extract → Chunk → Embed → Index (FAISS)
                ↓
           Retrieve → LLM → Insights 


##  Tech Stack

### Backend
- Python
- FastAPI
- PyMuPDF (PDF parsing)
- Sentence Transformers (embeddings)
- FAISS (vector search)
- Transformers (FLAN-T5 for generation)

### Frontend
- React (Vite)
- Tailwind CSS
- Axios (API communication)

---

##  API Endpoints

### Upload Document

POST /api/v1/upload


### Extract Document

GET /api/v1/extract/{document_id}


### Generate Summary

GET /api/v1/summary/{document_id}


### Semantic Search

POST /api/v1/search/{document_id}


### Question Answering

POST /api/v1/qa/{document_id}


### Analysis (Clauses / Risks / Fields)

GET /api/v1/analysis/{document_id}


---

##  Core Components

### Chunking Engine
- Overlapping chunk strategy
- Sentence-safe splitting
- Metadata tracking (page, offsets, length)

### Vector Pipeline
- Embeddings via `all-MiniLM-L6-v2`
- FAISS `IndexFlatIP` for similarity search
- Persistent index + metadata storage

### LLM Pipeline
- FLAN-T5 for:
  - Summarization
  - Question Answering
  - Structured insights
- Prompt-engineered for grounded responses

---

##  Current Status

- End-to-end pipeline (Upload → Insights)
- Fully working frontend + backend integration
- Real-time document processing
- Semantic retrieval + QA
- UI and intelligence improvements in progress

---

##  Roadmap

- Persistent metadata (timestamps, history)
- Improved clause classification (fine-tuned models)
- Risk scoring system
- Multi-document comparison
- User authentication & dashboards
- Deployment (Docker + cloud)

---

##  Motivation

ClauseIQ aims to simulate a real-world document intelligence system used in legal, compliance, and enterprise workflows — focusing on explainability, structured outputs, and grounded AI responses.