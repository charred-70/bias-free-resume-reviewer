from fastapi import APIRouter, UploadFile, File

from apps.api.app.services.resume_service import process_pdf

router = APIRouter()


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    path = f"/tmp/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return process_pdf(path)