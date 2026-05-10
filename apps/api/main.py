from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.app.routes import resume
from apps.api.app.routes import upload


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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