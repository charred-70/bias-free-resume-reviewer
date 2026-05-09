from fastapi import FastAPI
from apps.api.routes import resume

app = FastAPI()

app.include_router(resume.router)

@app.get("/")
def root():
    return {"message": "biasless-ai-platform running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "api",
        "version": "0.1.0"
    }