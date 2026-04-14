# ClauseIQ

ClauseIQ is a document intelligence system that extracts structured insights from PDFs and enables grounded question answering using local LLMs.

---

##  Why ClauseIQ?

Legal and business documents are often long, unstructured, and difficult to analyze manually.

ClauseIQ demonstrates how modern GenAI systems can:
- Transform raw documents into structured insights
- Enable grounded, explainable question answering
- Reduce manual review effort in legal/compliance workflows

This project simulates a real-world document intelligence system used in enterprise environments.

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


##  Example Use Case

Upload an NDA →  
- Extract clauses (Confidentiality, Termination, etc.)
- Identify potential risks  
- Ask: *“What is considered confidential information?”*  
- Get grounded answers with source references

## Screenshots

### DashBoard
![DashBoard](./assets/dashboard.png)

### Document Workspace
![Workspace](./assets/upload.png)

### Analysis Panel
![Analysis](./assets/analysis.png)


![Analysis](./assets/analysis1.png)


![Analysis](./assets/analysis2.png)


![Analysis](./assets/analysis3.png)

## Notes
- Uses local models (no paid APIs)
- Answers are grounded in document context
- Works best with structured PDFs

##  Future Improvements

- Real risk scoring using LLM outputs
- Multi-document comparison
- Document status auto-refresh (processing → ready)
- Authentication and user dashboards
- Cloud deployment (Docker + AWS/GCP)