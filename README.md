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