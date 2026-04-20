from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import upload, analyze, documents


app = FastAPI(title="ClauseIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1", tags=["Documents"])
app.include_router(analyze.router, prefix="/api/v1", tags=["Analyze"])
app.include_router(documents.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "ClauseIQ is running "}


@app.get("/health")
def health_check():
    return {"status": "ok"}
