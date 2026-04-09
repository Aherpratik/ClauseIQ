# ClauseIQ 

ClauseIQ is a backend system for intelligent document processing and analysis, designed to extract, structure, and prepare documents for advanced semantic understanding.

##  Features

-  Upload documents via API
-  Extract structured text from PDFs
-  Page-wise content extraction
-  FastAPI-based scalable backend
-  Clean JSON responses for downstream processing

##  Tech Stack

- Python
- FastAPI
- PyMuPDF (PDF parsing)
- Uvicorn

##  API Endpoints

### Upload Document

POST /api/v1/upload


### Extract Document

GET /api/v1/extract/{document_id}

## 🧩 Chunking Engine

Implemented a smart chunking pipeline that:
- Splits documents into overlapping chunks
- Preserves page context
- Avoids breaking sentences abruptly
- Stores metadata (page number, offsets, chunk length)

This prepares documents for downstream embedding and semantic retrieval.

## Current Progress

- PDF upload API
- Text extraction with PyMuPDF
- Page-wise document parsing
- Smart chunking with overlap
- Embedding generation with Sentence Transformers
- FAISS-based semantic retrieval
- Search endpoint for relevant chunk lookup

##  What's Next

- Vector embeddings
- Semantic search
- Clause detection engine

## 📌 Status

In active development (building toward a full GenAI-powered document intelligence system)