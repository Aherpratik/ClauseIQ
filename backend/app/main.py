from fastapi import FastAPI
from backend.app.api.v1 import upload

app = FastAPI(title="ClauseIQ API")

app.include_router(upload.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "ClauseIQ is running "}


@app.get("/health")
def health_check():
    return {"status": "ok"}
