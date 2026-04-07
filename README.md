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


##  What's Next

- Chunking pipeline
- Vector embeddings
- Semantic search
- Clause detection engine

## 📌 Status

In active development (building toward a full GenAI-powered document intelligence system)