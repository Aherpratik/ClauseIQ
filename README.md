# ClauseIQ

ClauseIQ is a document intelligence system that extracts structured insights from PDFs and enables grounded question answering using local LLMs.

---

##  Features

### Document Processing
- Upload PDF documents via API or UI
- Extract structured, page-wise text using PyMuPDF
- Smart chunking with overlap for better semantic understanding

### AI-Powered Analysis
- Automatic document summarization
- Clause extraction and categorization
- Risk identification (high / medium insights)
- Key field detection from legal and business documents

### Semantic Search
- Embedding-based retrieval using Sentence Transformers
- FAISS-powered vector search
- Relevant chunk retrieval for grounded responses

### Ask AI (RAG-based QA)
- Context-aware question answering over documents
- Uses retrieved chunks for grounded answers
- Reduces hallucination with constrained prompting

### Interactive Frontend (React + Tailwind)
- Workspace-style UI (similar to real SaaS tools)
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

```


##  Tech Stack

### Backend
- Python
- FastAPI
- PyMuPDF (PDF parsing)
- Sentence Transformers (embeddings)
- FAISS (vector search)
- HuggingFace (FLAN-T5)

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

GET /api/v1/analyze/{document_id}


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

## Getting Started

### Backend
```bash
cd backend
python -m venv clauseiq
source clauseiq/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Notes
- Uses local models (no paid APIs)
- Answers are grounded in document context
- Works best with structured PDFs

## Screenshots

### DashBoard
![DashBoard](../ClauseIQ/frontend/src/assets/dashboard.png)

### Document Workspace
![Workspace](../ClauseIQ/frontend/src/assets/upload.png)

### Analysis Panel
![Analysis](../ClauseIQ/frontend/src/assets/analysis.png)


![Analysis](../ClauseIQ/frontend/src/assets/analysis1.png)


![Analysis](../ClauseIQ/frontend/src/assets/analysis2.png)


![Analysis](../ClauseIQ/frontend/src/assets/analysis3.png)