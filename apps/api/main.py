from fastapi import FastAPI
from apps.api.app.routes import resume
from apps.api.app.routes import upload


app = FastAPI()

app.include_router(resume.router)
app.include_router(upload.router)

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