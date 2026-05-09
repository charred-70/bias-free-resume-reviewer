from fastapi import APIRouter
from apps.api.models.request_models import ResumeInput
from apps.api.services.resume_service import process_resume

router = APIRouter()

@router.post("/analyze")
def analyze_resume(data: ResumeInput):
    result = process_resume(data.resume_text)

    return {
        "cleaned_text": result["cleaned_text"],
        "length": result["length"]
    }

@router.get("/resume")
def get_resume():
    return {"message": "resume route working"}